from dataclasses import dataclass

from enums import ImportRuleFields


@dataclass
class ImportRule:
    id: int
    input_variable: str
    input_value: str
    output_variable: str
    output_value: str

    def __init__(
        self,
        input_variable: str,
        input_value: str,
        output_variable: str,
        output_value: str,
        id: int = -1,
    ):
        self.id = id
        self.input_variable = input_variable.lower()
        self.input_value = input_value.title()
        self.output_variable = output_variable.lower()
        self.output_value = output_value.title()

    @classmethod
    def from_sql_row(cls, row):
        return cls(
            id=row[ImportRuleFields.ID.value],
            input_variable=row[ImportRuleFields.INPUT_VARIABLE.value],
            input_value=row[ImportRuleFields.INPUT_VALUE.value],
            output_variable=row[ImportRuleFields.OUTPUT_VARIABLE.value],
            output_value=row[ImportRuleFields.OUTPUT_VALUE.value],
        )

    @property
    def params(self):
        """Does not include id"""
        return (
            self.input_variable,
            self.input_value,
            self.output_variable,
            self.output_value,
        )

    def __eq__(self, other):
        """Does not include id"""
        if not isinstance(other, ImportRule):
            return NotImplemented

        return (
            self.input_variable == other.self.input_variable
            and self.input_value == other.input_value
            and self.output_variable == other.output_variable
            and self.output_value == other.output_value
        )
