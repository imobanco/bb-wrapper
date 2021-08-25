class DACService:
    def mod_10(self, number):
        reversed_number = reversed(number)

        factor = 2
        total = 0
        for num in reversed_number:
            result = factor * int(num)
            result = sum([int(d) for d in str(result)])
            total += result
            factor = (factor % 2) + 1

        base = 10
        rest = total % base
        dv = base - rest
        if dv in [10]:
            dv = 0

        return str(dv)

    def mod_11(self, number):
        reversed_number = reversed(number)

        factor = 2
        total = 0
        for num in reversed_number:
            result = factor * int(num)
            total += result
            factor = (factor % 9) + 1 + (factor // 9) * 1

        base = 11
        rest = total % base
        dv = base - rest
        if dv in [0, 10, 11]:
            dv = 1

        return str(dv)
