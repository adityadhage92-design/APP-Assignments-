"""
=====================================================================
 SIMPLE REPORT GENERATOR  (Easy Version for 2nd Year Students)
 Topics covered: Decorators | classmethod | Magic Methods (dunder)
=====================================================================
This program shows 3 Python OOP concepts using a very simple
example: making a small "Report" with sections (like a mini
project report with Introduction, Result, Conclusion etc.)

Concept 1: DECORATORS
   - A decorator is a function that adds extra work around
     another function, without changing that function's code.
   - Example: adding "**" around text, or making text UPPERCASE.

Concept 2: CLASSMETHOD
   - A normal method works on ONE object (self).
   - A classmethod works on the CLASS itself (cls), so it can
     be used to create objects in a special way, or store data
     shared by ALL objects of that class.

Concept 3: MAGIC METHODS (also called dunder methods, "dunder"
   = Double UNDERscore, like __init__, __str__)
   - These are special methods Python calls AUTOMATICALLY when
     you use normal Python operators/syntax like print(), len(),
     for loops, +, ==, etc. on your own class.
=====================================================================
"""


# =====================================================================
# PART 1: DECORATORS
# =====================================================================

# A decorator function takes another function as input,
# and returns a new function with extra behaviour added.

def uppercase(func):
    """Makes the text returned by func() become UPPERCASE."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)   # run the original function
        return result.upper()             # add extra behaviour
    return wrapper


def bold(func):
    """Adds ** before and after the text (like bold in markdown)."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return "**" + result + "**"
    return wrapper


def add_border(func):
    """Adds a line of dashes above and below the text."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        border = "-" * 40
        return border + "\n" + result + "\n" + border
    return wrapper


# =====================================================================
# PART 2: THE REPORT CLASS
# =====================================================================

class Report:
    """A simple report made up of a title and a list of sections."""

    # ---------------------------------------------------------
    # CLASS VARIABLE
    # This variable is shared by ALL Report objects (not just
    # one). We use it to store report templates that anyone can
    # reuse (like a "form" you fill later).
    # ---------------------------------------------------------
    templates = {}

    def __init__(self, title, author="Unknown"):
        self.title = title
        self.author = author
        self.sections = []          # list of (heading, content) pairs

    # ---------------------------------------------------------
    # CLASSMETHOD EXAMPLE 1
    # Notice: first argument is "cls", not "self".
    # This method changes data that belongs to the CLASS
    # (templates dictionary), which is shared by everyone.
    # ---------------------------------------------------------
    @classmethod
    def add_template(cls, name, section_list):
        cls.templates[name] = section_list
        print(f"Template '{name}' saved with sections: {section_list}")

    # ---------------------------------------------------------
    # CLASSMETHOD EXAMPLE 2 (Alternate Constructor)
    # A normal way to create an object is: Report("Title")
    # This classmethod gives ANOTHER way to create an object,
    # directly using an already saved template.
    # ---------------------------------------------------------
    @classmethod
    def create_from_template(cls, template_name, title, author="Unknown"):
        new_report = cls(title, author)   # cls(...) = Report(...)
        for heading in cls.templates[template_name]:
            new_report.add_section(heading, "content not filled yet")
        return new_report

    # ---------------------------------------------------------
    # Normal instance method - adds one section to this report
    # ---------------------------------------------------------
    def add_section(self, heading, content):
        self.sections.append((heading, content))

    def fill_section(self, heading, content):
        """Update the content of a section that already exists."""
        for i in range(len(self.sections)):
            if self.sections[i][0] == heading:
                self.sections[i] = (heading, content)
                return True
        return False

    # ---------------------------------------------------------
    # This normal method is wrapped with TWO decorators.
    # Decorators apply bottom-up:
    #   1. add_border runs first -> adds the dashed lines
    #   2. bold runs next -> adds ** around the bordered text
    # ---------------------------------------------------------
    @bold
    @add_border
    def summary(self):
        return f"Report: {self.title} | Author: {self.author} | Sections: {len(self.sections)}"

    # =========================================================
    # MAGIC METHODS
    # These special methods are never called by us directly.
    # Python calls them AUTOMATICALLY when we use print(),
    # len(), for loop, +, == etc. on a Report object.
    # =========================================================

    def __str__(self):
        # Called automatically when we do: print(report_object)
        text = f"REPORT: {self.title} (by {self.author})\n"
        for heading, content in self.sections:
            text += f" - {heading}: {content}\n"
        return text

    def __len__(self):
        # Called automatically when we do: len(report_object)
        return len(self.sections)

    def __getitem__(self, index):
        # Called automatically when we do: report_object[0]
        return self.sections[index]

    def __add__(self, other):
        # Called automatically when we do: report1 + report2
        combined = Report(self.title + " + " + other.title, self.author)
        combined.sections = self.sections + other.sections
        return combined

    def __eq__(self, other):
        # Called automatically when we do: report1 == report2
        return self.title == other.title and self.sections == other.sections


# =====================================================================
# PART 3: DEMO CODE (this runs only when file is executed directly)
# =====================================================================
if __name__ == "__main__":

    # ---- Using classmethod to save a template ----
    Report.add_template("project_report", ["Introduction", "Result", "Conclusion"])

    # ---- Using classmethod as an alternate constructor ----
    r1 = Report.create_from_template("project_report", "My Mini Project", "Rahul")
    r1.fill_section("Introduction", "This project shows OOP concepts in Python.")
    r1.fill_section("Result", "The program worked correctly.")
    r1.fill_section("Conclusion", "Decorators and magic methods make code flexible.")

    # ---- Creating a second report normally ----
    r2 = Report("Attendance Report", "Rahul")
    r2.add_section("Summary", "92% attendance this month.")

    # ---- Magic methods in action ----
    print("---- print(r1) uses __str__ ----")
    print(r1)

    print("---- len(r1) uses __len__ ----")
    print(len(r1))

    print("---- r1[0] uses __getitem__ ----")
    print(r1[0])

    print("---- r1 + r2 uses __add__ ----")
    combined = r1 + r2
    print(combined)

    print("---- r1 == r1 uses __eq__ ----")
    print(r1 == r1)

    # ---- Decorators in action ----
    print("---- summary() with @bold and @add_border decorators ----")
    print(r1.summary())
