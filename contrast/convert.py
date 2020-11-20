from contrast.calculate import Calculate

class Convert:
    def reverseTransformation(self, c):
        if (c < 0.0002):
            return 0.0002;
        elif (c > 0.04045):
            return pow((c + 0.055) / (1.055), 2.4);
        else:
            return c / 12.92;

    def transformation(self, c):
        if (c < 0.0002):
            return 0.0002;
        elif (c > 0.003131594552688991):
            return (pow(c, 1 / 2.4) * 1.055) - 0.055;
        else:
            return c * 12.92;

    def transform(self, color, contrast):
        color[0] = self.reverseTransformation(color[0]);
        color[1] = self.reverseTransformation(color[1]);
        color[2] = self.reverseTransformation(color[2]);

        constant = Calculate().constant(color, contrast);

        return [
            self.transformation(constant[0] * color[0]),
            self.transformation(constant[1] * color[1]),
            self.transformation(constant[2] * color[2]),
        ]

