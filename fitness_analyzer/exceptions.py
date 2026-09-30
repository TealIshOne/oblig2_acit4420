"""
errorhandeling and raised 'personalised' exveptions
"""


class InvalidIdentifierError(ValueError):
    def __init__(self, identifier, id_type, expected_pattern):
        self.identifier=identifier
        self.id_type=id_type
        self.excpected_pattern= expected_pattern
        message=(
            f"invalid {id_type}: '{identifier}'",
            f"does not match excpected pattern {expected_pattern}"
        )
        super().__init(message)



class InvalidRecordError(ValueError):
    def __init__(self, reason,field=None, row_num=None, source_file=None):
        self.reason=reason
        self.field=field
        self.row_num=row_num
        self.source_file=source_file

        message=f"invalid record"
        if field:
            message+=f" (field: {field})"
        if row_num:
            message+= f"at row {row_num}"
        if source_file:
            message+= f"in {source_file}"
        message+= f": {reason}"

        super().__init__(message)