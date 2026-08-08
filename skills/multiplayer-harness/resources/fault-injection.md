# Fault injection profiles

Record the intended profile in scenario `conditions`, then use reviewed `fault_on` and `fault_off` argv-array actions to control the platform/provider tool actually available.

Suggested correctness profiles:

| Profile | Latency | Jitter | Loss | Notes |
|---|---:|---:|---:|---|
| baseline | 0 ms | 0 ms | 0% | Production topology without shaping |
| regional | 80 ms | 15 ms | 0.5% | Ordinary remote-session stress |
| degraded | 180 ms | 40 ms | 3% | Prediction, timeout and retry behavior |
| hostile-mobile | 300 ms | 100 ms | 8% | Expected degradation/disconnect boundaries |

Use provider-supported simulation when it exercises the intended transport path. Otherwise use an OS tool appropriate to the host, such as Linux `tc netem`, a reviewed Windows packet-shaping tool, macOS `dnctl`, or a controlled proxy. These tools have different privilege and interface-selection requirements; never generate or execute a privileged command without reviewing the exact adapter, target interface/process and teardown.

Always restore network state in teardown, even after test failure. Capture the shaping tool/version, applied command, target, start/end timestamps and verification output. If shaping cannot be verified, mark the scenario `inconclusive` rather than claiming the requested latency/loss occurred.
