from langchain.schema import HumanMessage, AIMessage
from typing import Dict, Any, List
import datetime


def log(message: str, error: bool = False):
    prefix = "[ERROR]" if error else "[INFO]"
    print(f"{prefix} {message}")


class LangSmithTracer:
    """
    LangSmith-like tracer for logging conversation runs, inputs, outputs,
    states, and evaluations with a convenient logger method.
    """

    def __init__(self):
        # Store conversation traces keyed by conversation_id
        self.traces: Dict[str, List[Dict[str, Any]]] = {}

    def start_trace(self, conversation_id: str, input_text: str, stage: str):
        """Begin a new trace entry for a conversation stage."""
        trace_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "stage": stage,
            "input": input_text,
            "output": None,
            "state": None,
            "evaluation": None,
        }
        self.traces.setdefault(conversation_id, []).append(trace_entry)
        log(f"[{conversation_id}] Started trace at stage '{stage}' with input: {input_text}")
        return trace_entry

    def end_trace(self, conversation_id: str, output_text: str, state: dict):
        """Complete the last trace entry with output and state info."""
        if conversation_id not in self.traces or not self.traces[conversation_id]:
            log(f"[{conversation_id}] Warning: No trace started for this conversation to end.", error=True)
            return

        trace_entry = self.traces[conversation_id][-1]
        trace_entry["output"] = output_text
        trace_entry["state"] = state.copy()
        log(f"[{conversation_id}] Ended trace with output: {output_text} and state: {state}")

    def add_evaluation(self, conversation_id: str, evaluation: dict):
        """Add an evaluation (e.g., correctness, relevance) to the last trace."""
        if conversation_id not in self.traces or not self.traces[conversation_id]:
            log(f"[{conversation_id}] Warning: No trace started for this conversation to add evaluation.",
                     error=True)
            return

        self.traces[conversation_id][-1]["evaluation"] = evaluation
        log(f"[{conversation_id}] Added evaluation: {evaluation}")

    def get_conversation_traces(self, conversation_id: str):
        """Retrieve all traces for a given conversation."""
        return self.traces.get(conversation_id, [])

    def print_traces(self, conversation_id: str):
        """Print all traces for debugging."""
        traces = self.get_conversation_traces(conversation_id)
        if not traces:
            log(f"[{conversation_id}] No traces found.")
            return
        log(f"[{conversation_id}] Printing all traces:")
        for i, trace in enumerate(traces, 1):
            print(f"Trace {i} - Stage: {trace['stage']}")
            print(f"  Input: {trace['input']}")
            print(f"  Output: {trace['output']}")
            print(f"  State: {trace['state']}")
            print(f"  Evaluation: {trace['evaluation']}")
            print(f"  Timestamp: {trace['timestamp']}\n")
