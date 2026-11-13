# Walkthrough

90 seconds: (0–20) Explain finite symbols and the zero-gradient construction. (20–45) Open compiler, scrub a real write, inspect its coordinate and checksum. (45–65) Open evidence and show the length-256 degradation. (65–90) Show patch drift and explain what remains untested.

Three minutes: add the oracle/forward separation, normal-equation derivation, baseline architecture mismatch, and a reproducibility command. End with the architecture-matched experiment.

Skeptical questions: Is this a standard transformer? No. Is the editor a real LM repair? No. Does low rank mean few changed entries? No; inspect C5. Is 100% a general security claim? No, it is conditional on this finite generator.