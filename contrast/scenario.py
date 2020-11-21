class Scenario:
    def Red(self, constant, minConstant, maxConstant):
        return minConstant[0] > constant[0] or maxConstant[0] < constant[0];

    def Green(self, constant, minConstant, maxConstant):
        return minConstant[1] > constant[1] or maxConstant[1] < constant[1];

    def Blue(self, constant, minConstant, maxConstant):
        return minConstant[2] > constant[2] or maxConstant[2] < constant[2];

    def RedGreen(self, constant, minConstant, maxConstant):
        return self.Red(constant, minConstant, maxConstant) and self.Green(constant, minConstant, maxConstant);
    
    def RedBlue(self, constant, minConstant, maxConstant):
        return self.Red(constant, minConstant, maxConstant) and self.Blue(constant, minConstant, maxConstant);
    
    def GreenBlue(self, constant, minConstant, maxConstant):
        return self.Green(constant, minConstant, maxConstant) and self.Blue(constant, minConstant, maxConstant);