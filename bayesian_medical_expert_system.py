import tkinter as tk
from tkinter import ttk

# Bayesian Medical Expert System
# Educational prototype using Python and Tkinter.
# The probabilities below are illustrative and are not for real diagnosis.

BG = "#F3F6FB"
NAVY = "#172554"
BLUE = "#3157D5"
PALE_BLUE = "#E8EEFF"
WHITE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#64748B"
GREEN = "#15803D"
RED = "#B91C1C"
AMBER = "#B45309"


class MedicalExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bayesian Medical Expert System")
        self.root.geometry("1120x760")
        self.root.minsize(940, 680)
        self.root.configure(bg=BG)

        self.fever = tk.StringVar(value="Yes")
        self.cough = tk.StringVar(value="Yes")
        self.fatigue = tk.StringVar(value="Yes")

        self.setup_style()
        self.build_ui()
        self.calculate_diagnosis()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox", fieldbackground=WHITE, background=WHITE,
            foreground=TEXT, padding=8, font=("Segoe UI", 10)
        )
        style.map("TCombobox", fieldbackground=[("readonly", WHITE)])
        style.configure(
            "Horizontal.TProgressbar", troughcolor="#E2E8F0",
            background=BLUE, bordercolor="#E2E8F0", thickness=12
        )

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=NAVY, height=105)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="✚  AI HEALTH SUPPORT", bg=NAVY, fg="#A5B4FC",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=28, pady=(15, 2))
        tk.Label(header, text="Bayesian Medical Expert System", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=28)
        tk.Label(header, text="PROBABILISTIC DIAGNOSIS  •  BAYESIAN BELIEF NETWORK",
                 bg=NAVY, fg="#CBD5E1", font=("Segoe UI", 9, "bold")).place(
                     relx=1, x=-28, y=51, anchor="e")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=20)

        # Symptom selection panel
        left = tk.Frame(body, bg=WHITE, highlightbackground="#E2E8F0",
                        highlightthickness=1, width=300)
        left.pack(side="left", fill="y", padx=(0, 18))
        left.pack_propagate(False)

        tk.Label(left, text="PATIENT EVIDENCE", bg=WHITE, fg=BLUE,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(22, 5))
        tk.Label(left, text="Select symptoms", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=20)
        tk.Label(left, text="Choose Yes or No for each observed symptom.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 9),
                 wraplength=250, justify="left").pack(anchor="w", padx=20, pady=(6, 20))

        self.add_symptom_field(left, "Fever", self.fever)
        self.add_symptom_field(left, "Cough", self.cough)
        self.add_symptom_field(left, "Fatigue", self.fatigue)

        tk.Frame(left, bg="#E2E8F0", height=1).pack(fill="x", padx=20, pady=17)

        tk.Button(left, text="  Calculate Diagnosis  →",
                  command=self.calculate_diagnosis, bg=BLUE, fg=WHITE,
                  activebackground="#2445B8", activeforeground=WHITE,
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 11, "bold"), pady=12).pack(fill="x", padx=20)

        tk.Button(left, text="Clear / Reset", command=self.reset,
                  bg=PALE_BLUE, fg=BLUE, activebackground="#DCE5FF",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"), pady=10).pack(
                      fill="x", padx=20, pady=(9, 0))

        tk.Label(left, text="BAYESIAN NETWORK", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=20, pady=(22, 5))
        tk.Label(left, text="             Flu\\n          ↙   ↓   ↘\\n      Fever  Cough  Fatigue",
                 bg=WHITE, fg=TEXT, font=("Consolas", 10),
                 justify="left").pack(anchor="w", padx=20)
        tk.Label(left, text="Prior probability: Flu = 30%",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(
                     anchor="w", padx=20, pady=(10, 0))

        # Results dashboard
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Diagnosis dashboard", bg=BG, fg=TEXT,
                 font=("Segoe UI", 19, "bold")).pack(anchor="w")
        tk.Label(right, text="Bayesian inference updates the disease probability using symptoms.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 15))

        cards = tk.Frame(right, bg=BG)
        cards.pack(fill="x")
        self.flu_card = self.metric_card(cards, "POSTERIOR: FLU", "—", RED)
        self.flu_card.pack(side="left", fill="both", expand=True, padx=(0, 9))
        self.no_flu_card = self.metric_card(cards, "POSTERIOR: NO FLU", "—", GREEN)
        self.no_flu_card.pack(side="left", fill="both", expand=True, padx=(0, 9))
        self.update_card = self.metric_card(cards, "PROBABILITY UPDATE", "—", BLUE)
        self.update_card.pack(side="left", fill="both", expand=True)

        probability_panel = tk.Frame(right, bg=WHITE, highlightbackground="#E2E8F0",
                                     highlightthickness=1)
        probability_panel.pack(fill="x", pady=(16, 13))
        tk.Label(probability_panel, text="POSTERIOR PROBABILITY DISTRIBUTION",
                 bg=WHITE, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(
                     anchor="w", padx=18, pady=(15, 4))
        tk.Label(probability_panel, text="Probability of Flu after considering the selected evidence",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=18)
        self.flu_probability_label = tk.Label(
            probability_panel, text="—", bg=WHITE, fg=BLUE,
            font=("Segoe UI", 26, "bold"))
        self.flu_probability_label.pack(anchor="w", padx=18, pady=(7, 5))
        self.progress = ttk.Progressbar(
            probability_panel, maximum=100, style="Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=18, pady=(0, 15))

        lower = tk.Frame(right, bg=BG)
        lower.pack(fill="both", expand=True)

        evidence_panel = tk.Frame(lower, bg=WHITE, highlightbackground="#E2E8F0",
                                  highlightthickness=1)
        evidence_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(evidence_panel, text="Observed symptoms", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=16, pady=(14, 7))
        self.evidence_output = tk.Label(
            evidence_panel, text="", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 10), justify="left")
        self.evidence_output.pack(anchor="w", padx=16, pady=(0, 12))

        reasoning_panel = tk.Frame(lower, bg=WHITE, highlightbackground="#E2E8F0",
                                   highlightthickness=1)
        reasoning_panel.pack(side="left", fill="both", expand=True)
        tk.Label(reasoning_panel, text="Decision support", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=16, pady=(14, 7))
        self.decision_title = tk.Label(
            reasoning_panel, text="", bg=WHITE, fg=BLUE,
            font=("Segoe UI", 11, "bold"), wraplength=260, justify="left")
        self.decision_title.pack(anchor="w", padx=16)
        self.reasoning_output = tk.Label(
            reasoning_panel, text="", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 9), wraplength=260, justify="left")
        self.reasoning_output.pack(anchor="w", padx=16, pady=(5, 12))

        tk.Label(self.root,
                 text="Educational demonstration only — not a real medical diagnosis. Consult a qualified healthcare professional.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(pady=(0, 9))

    def add_symptom_field(self, parent, label, variable):
        frame = tk.Frame(parent, bg=WHITE)
        frame.pack(fill="x", padx=20, pady=(0, 13))
        tk.Label(frame, text=label, bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Combobox(frame, textvariable=variable, values=["Yes", "No"],
                     state="readonly", font=("Segoe UI", 10)).pack(fill="x")

    def metric_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=WHITE, highlightbackground="#E2E8F0",
                        highlightthickness=1, padx=12, pady=14)
        tk.Label(card, text=title, bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        number = tk.Label(card, text=value, bg=WHITE, fg=color,
                          font=("Segoe UI", 17, "bold"))
        number.pack(anchor="w", pady=(7, 0))
        card.number_label = number
        return card

    def calculate_diagnosis(self):
        # Prior probabilities
        p_flu = 0.30
        p_no_flu = 0.70

        # Conditional probabilities:
        # P(Fever=Yes | Flu)=0.80, P(Fever=Yes | No Flu)=0.20
        # P(Cough=Yes | Flu)=0.75, P(Cough=Yes | No Flu)=0.30
        # P(Fatigue=Yes | Flu)=0.70, P(Fatigue=Yes | No Flu)=0.25
        symptom_data = [
            ("Fever", self.fever.get(), 0.80, 0.20),
            ("Cough", self.cough.get(), 0.75, 0.30),
            ("Fatigue", self.fatigue.get(), 0.70, 0.25),
        ]

        flu_joint = p_flu
        no_flu_joint = p_no_flu

        for _, answer, p_yes_flu, p_yes_no_flu in symptom_data:
            if answer == "Yes":
                flu_joint *= p_yes_flu
                no_flu_joint *= p_yes_no_flu
            else:
                flu_joint *= (1 - p_yes_flu)
                no_flu_joint *= (1 - p_yes_no_flu)

        total = flu_joint + no_flu_joint
        flu_percent = (flu_joint / total) * 100 if total else 0
        no_flu_percent = 100 - flu_percent
        update = flu_percent - 30.0

        self.flu_card.number_label.config(text=f"{flu_percent:.2f}%")
        self.no_flu_card.number_label.config(text=f"{no_flu_percent:.2f}%")
        self.update_card.number_label.config(
            text=f"{update:+.2f} percentage points")
        self.flu_probability_label.config(text=f"{flu_percent:.2f}%")
        self.progress["value"] = flu_percent

        self.evidence_output.config(
            text=f"• Fever: {self.fever.get()}\\n"
                 f"• Cough: {self.cough.get()}\\n"
                 f"• Fatigue: {self.fatigue.get()}"
        )

        if flu_percent >= 70:
            decision = "Higher probability of Flu"
            color = RED
            recommendation = "The selected symptoms increase the model's estimated probability. Consider professional clinical evaluation."
        elif flu_percent >= 40:
            decision = "Moderate probability"
            color = AMBER
            recommendation = "The evidence gives an intermediate estimate. Symptoms alone cannot confirm a disease."
        else:
            decision = "Lower probability of Flu"
            color = GREEN
            recommendation = "The selected evidence gives a lower estimate in this model. A low estimate does not rule out illness."

        self.decision_title.config(text=decision, fg=color)
        self.reasoning_output.config(
            text=f"{recommendation}\\n\\n"
                 f"Prior P(Flu) = 30.00%\\n"
                 f"Posterior P(Flu | evidence) = {flu_percent:.2f}%\\n\\n"
                 "The model multiplies the prior by the conditional likelihood of each symptom, "
                 "then normalizes Flu and No Flu scores using Bayes' theorem."
        )

    def reset(self):
        self.fever.set("No")
        self.cough.set("No")
        self.fatigue.set("No")
        self.calculate_diagnosis()


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalExpertSystem(root)
    root.mainloop()
