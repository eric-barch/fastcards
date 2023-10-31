from global_vars import column_widths


class Note:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return (
            f"{'source: ' + self.source:<{column_widths[1]}}"
            f"{'target: ' + self.target:<{column_widths[2]}}"
        )
