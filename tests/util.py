class StartsWithAssertion(object):
    def assertStartsWith(self, a, b):
        self.assertTrue(
            b.startswith(a),
            '{0} does not start with {1}'.format(b, a)
        )


class IOStubs(object):
    def yes_input(self, output):
        self.log_output(output)
        return 'y'

    def no_input(self, output):
        self.log_output(output)
        return 'n'

    def eventual_yes_input(self, output):
        self.log_output(output)
        self.unknown_inputs_count += 1
        if self.unknown_inputs_count >= 3:
            return 'y'
        return 'unknown'

    def log_output(self, *items):
        self.log.append(*items)

    def full_log(self):
        return "\n".join(self.log)

    def clear_log(self):
        self.log = []

    def clear_unknown_inputs_count(self):
        self.unknown_inputs_count = 0
