#!/usr/bin/env python3
"""Scenario-driven, provider-neutral multiplayer process laboratory.

Commands are always argv arrays and never executed through a shell. Network shaping is
delegated to explicit fault-controller commands because OS/provider capabilities and
privilege requirements differ.
"""
from __future__ import annotations

import argparse
import json
import os
import queue
import re
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


TERMINAL_RESULTS = {"passed", "failed", "timeout", "inconclusive"}


def utc_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def expand(value: str, variables: dict[str, str]) -> str:
    result = value
    for key, replacement in variables.items():
        result = result.replace("${" + key + "}", replacement)
    if "${" in result:
        raise ValueError(f"unresolved variable in {value!r}")
    return result


def expanded_argv(command: list[Any], variables: dict[str, str]) -> list[str]:
    if not isinstance(command, list) or not command:
        raise ValueError("command must be a non-empty argv array")
    return [expand(str(part), variables) for part in command]


@dataclass
class ProcessState:
    spec: dict[str, Any]
    process: subprocess.Popen[str] | None = None
    generation: int = 0
    started_at: float | None = None
    ready_at: float | None = None
    completed_at: float | None = None
    ready: bool = False
    completed: bool = False
    expected_stop: bool = False
    exit_code: int | None = None
    failure: str | None = None
    logs: list[str] = field(default_factory=list)
    log_file: Any = None

    @property
    def name(self) -> str:
        return str(self.spec["name"])


class MultiplayerLab:
    def __init__(self, scenario: dict[str, Any], output: Path) -> None:
        self.scenario = scenario
        self.output = output
        self.artifact_dir = output.parent / (output.stem + "-artifacts")
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        self.events: queue.Queue[tuple[str, int, str]] = queue.Queue()
        self.processes = {str(spec["name"]): ProcessState(spec) for spec in scenario["processes"]}
        self.start_monotonic = time.monotonic()
        self.actions = sorted(scenario.get("actions", []), key=lambda item: float(item.get("atSeconds", 0)))
        self.action_results: list[dict[str, Any]] = []
        self.failures: list[dict[str, Any]] = []
        self.fault_teardowns: list[list[str]] = []
        self.variables = {str(k): str(v) for k, v in scenario.get("variables", {}).items()}
        self.variables.setdefault("SCENARIO", str(scenario.get("name", "scenario")))
        self.variables.setdefault("SEED", str(scenario.get("seed", 0)))

    def elapsed(self) -> float:
        return time.monotonic() - self.start_monotonic

    def reader(self, state: ProcessState, generation: int) -> None:
        assert state.process is not None and state.process.stdout is not None
        for raw in iter(state.process.stdout.readline, ""):
            line = raw.rstrip("\r\n")
            state.logs.append(line)
            if len(state.logs) > 1000:
                del state.logs[: len(state.logs) - 1000]
            if state.log_file:
                state.log_file.write(line + "\n")
                state.log_file.flush()
            self.events.put((state.name, generation, line))

    def start(self, name: str) -> None:
        state = self.processes[name]
        if state.process is not None and state.process.poll() is None:
            raise RuntimeError(f"process {name} is already running")
        local_vars = dict(self.variables)
        local_vars.update({"NAME": name, "ROLE": str(state.spec.get("role", "peer")), "GENERATION": str(state.generation + 1)})
        command = expanded_argv(state.spec["command"], local_vars)
        env = os.environ.copy()
        env.update({str(k): expand(str(v), local_vars) for k, v in state.spec.get("env", {}).items()})
        cwd = state.spec.get("cwd")
        if cwd:
            cwd = expand(str(cwd), local_vars)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        state.generation += 1
        state.ready = not bool(state.spec.get("readyRegex"))
        state.completed = not bool(state.spec.get("completeRegex"))
        state.expected_stop = False
        state.failure = None
        state.exit_code = None
        state.started_at = self.elapsed()
        state.ready_at = state.started_at if state.ready else None
        state.completed_at = state.started_at if state.completed else None
        log_path = self.artifact_dir / f"{name}-g{state.generation}.log"
        state.log_file = log_path.open("w", encoding="utf-8")
        state.process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, creationflags=creationflags)
        threading.Thread(target=self.reader, args=(state, state.generation), daemon=True).start()

    def stop(self, name: str, expected: bool = True) -> None:
        state = self.processes[name]
        state.expected_stop = expected
        process = state.process
        if process is None or process.poll() is not None:
            return
        try:
            if os.name == "nt":
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                process.terminate()
            process.wait(timeout=float(state.spec.get("graceSeconds", 5)))
        except (subprocess.TimeoutExpired, OSError):
            process.kill()
            process.wait(timeout=5)
        finally:
            state.exit_code = process.poll()
            if state.log_file:
                state.log_file.close()
                state.log_file = None

    def restart(self, name: str) -> None:
        self.stop(name, expected=True)
        delay = float(self.processes[name].spec.get("restartDelaySeconds", 0.1))
        if delay > 0:
            time.sleep(delay)
        self.start(name)

    def run_command(self, command: list[Any], label: str) -> dict[str, Any]:
        argv = expanded_argv(command, self.variables)
        started = self.elapsed()
        completed = subprocess.run(argv, capture_output=True, text=True, timeout=float(self.scenario.get("commandTimeoutSeconds", 30)), check=False)
        result = {"label": label, "command": argv, "exitCode": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:], "atSeconds": round(started, 3)}
        if completed.returncode != 0:
            self.failures.append({"kind": "command", "process": label, "detail": f"exit {completed.returncode}"})
        return result

    def run_action(self, action: dict[str, Any]) -> None:
        kind = str(action["type"])
        target = action.get("target")
        record: dict[str, Any] = {"type": kind, "target": target, "scheduledSeconds": action.get("atSeconds", 0), "actualSeconds": round(self.elapsed(), 3), "status": "passed"}
        try:
            if kind == "start": self.start(str(target))
            elif kind == "stop": self.stop(str(target), expected=True)
            elif kind == "restart": self.restart(str(target))
            elif kind == "fault_on":
                result = self.run_command(action["command"], "fault_on")
                record["commandResult"] = result
                teardown = action.get("teardownCommand")
                if teardown: self.fault_teardowns.append(expanded_argv(teardown, self.variables))
                if result["exitCode"] != 0: record["status"] = "failed"
            elif kind == "fault_off":
                result = self.run_command(action["command"], "fault_off")
                record["commandResult"] = result
                if result["exitCode"] != 0: record["status"] = "failed"
            else: raise ValueError(f"unsupported action type {kind}")
        except Exception as error:
            record["status"] = "failed"
            record["error"] = f"{type(error).__name__}: {error}"
            self.failures.append({"kind": "action", "process": str(target or ""), "detail": record["error"]})
        self.action_results.append(record)

    def process_line(self, name: str, generation: int, line: str) -> None:
        state = self.processes[name]
        if generation != state.generation:
            return
        ready_regex = state.spec.get("readyRegex")
        complete_regex = state.spec.get("completeRegex")
        failure_regex = state.spec.get("failureRegex")
        if ready_regex and not state.ready and re.search(str(ready_regex), line):
            state.ready, state.ready_at = True, self.elapsed()
        if complete_regex and not state.completed and re.search(str(complete_regex), line):
            state.completed, state.completed_at = True, self.elapsed()
        if failure_regex and re.search(str(failure_regex), line):
            state.failure = line
            self.failures.append({"kind": "log", "process": name, "detail": line})

    def start_eligible(self) -> None:
        for state in self.processes.values():
            if not state.spec.get("autoStart", True) or state.generation or state.process is not None:
                continue
            dependencies = [str(x) for x in state.spec.get("startAfterReady", [])]
            if all(self.processes[name].ready for name in dependencies):
                self.start(state.name)

    def update_exits(self) -> None:
        for state in self.processes.values():
            if state.process is None or state.exit_code is not None:
                continue
            code = state.process.poll()
            if code is None:
                continue
            state.exit_code = code
            if state.log_file:
                state.log_file.close(); state.log_file = None
            if state.spec.get("required", True) and not state.expected_stop and not state.completed:
                state.failure = f"unexpected exit {code}"
                self.failures.append({"kind": "exit", "process": state.name, "detail": state.failure})

    def success_ready(self) -> bool:
        if len(self.action_results) < len(self.actions): return False
        for state in self.processes.values():
            if state.spec.get("required", True) and not state.ready: return False
            if state.spec.get("completeRegex") and state.spec.get("required", True) and not state.completed: return False
        return not self.failures

    def run(self) -> dict[str, Any]:
        timeout = float(self.scenario.get("timeoutSeconds", 120))
        next_action = 0
        result = "inconclusive"
        try:
            while self.elapsed() < timeout:
                self.start_eligible()
                while next_action < len(self.actions) and self.elapsed() >= float(self.actions[next_action].get("atSeconds", 0)):
                    self.run_action(self.actions[next_action]); next_action += 1
                try:
                    while True:
                        self.process_line(*self.events.get_nowait())
                except queue.Empty:
                    pass
                self.update_exits()
                if self.failures:
                    result = "failed"; break
                if self.success_ready():
                    result = "passed"; break
                time.sleep(0.02)
            else:
                result = "timeout"
        finally:
            for name in reversed(list(self.processes)):
                self.stop(name, expected=True)
            for command in reversed(self.fault_teardowns):
                try: subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
                except Exception as error: self.failures.append({"kind": "fault_teardown", "process": "", "detail": str(error)})
        if result == "passed" and self.failures: result = "failed"
        report = self.report(result)
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    def report(self, result: str) -> dict[str, Any]:
        if result not in TERMINAL_RESULTS: result = "inconclusive"
        process_results = []
        for state in self.processes.values():
            process_results.append({"name": state.name, "role": state.spec.get("role", "peer"), "generation": state.generation, "ready": state.ready, "completed": state.completed, "startedSeconds": state.started_at, "readySeconds": state.ready_at, "completedSeconds": state.completed_at, "exitCode": state.exit_code, "failure": state.failure, "logTail": state.logs[-80:]})
        return {"schemaVersion": 2, "scenario": self.scenario.get("name", "scenario"), "scenarioId": self.scenario.get("id", ""), "seed": self.scenario.get("seed", 0), "startedUtc": utc_now(), "durationSeconds": round(self.elapsed(), 3), "topology": self.scenario.get("topology", "custom"), "build": self.scenario.get("build", {}), "conditions": self.scenario.get("conditions", {}), "result": result, "processes": process_results, "actions": self.action_results, "metrics": {}, "failures": self.failures, "artifacts": [str(self.artifact_dir)]}


def validate_scenario(data: dict[str, Any]) -> None:
    if int(data.get("schemaVersion", 0)) != 1: raise ValueError("scenario schemaVersion must be 1")
    processes = data.get("processes")
    if not isinstance(processes, list) or not processes: raise ValueError("scenario requires processes")
    names = [str(item.get("name", "")) for item in processes]
    if any(not name for name in names) or len(names) != len(set(names)): raise ValueError("process names must be non-empty and unique")
    base_variables = {str(k): str(v) for k, v in data.get("variables", {}).items()}
    base_variables.setdefault("SCENARIO", str(data.get("name", "scenario")))
    base_variables.setdefault("SEED", str(data.get("seed", 0)))
    for item in processes:
        item_variables = dict(base_variables)
        item_variables.update({"NAME": item["name"], "ROLE": item.get("role", "peer"), "GENERATION": "1"})
        expanded_argv(item.get("command", []), item_variables)
        for dependency in item.get("startAfterReady", []):
            if dependency not in names: raise ValueError(f"unknown dependency {dependency}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--out", type=Path, default=Path("Temp/UnityArchitectPro/multiplayer-lab-result.json"))
    args = parser.parse_args()
    scenario = json.loads(args.scenario.read_text(encoding="utf-8"))
    validate_scenario(scenario)
    report = MultiplayerLab(scenario, args.out).run()
    print(args.out)
    print(report["result"])
    return 0 if report["result"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
