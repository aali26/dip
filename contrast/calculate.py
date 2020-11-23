from contrast.scenario import Scenario

class Calculate:
    def __init__(self):
        self.MIN_CONSTANT_VALUE = 0.001 / 256;

    def MinConstant(self, color):
        return [
            self.MIN_CONSTANT_VALUE / color[0],
            self.MIN_CONSTANT_VALUE / color[1],
            self.MIN_CONSTANT_VALUE / color[2],
        ]

    def MaxConstant(self, color):
        return [
            1 / color[0],
            1 / color[1],
            1 / color[2],
        ]

    def set(self, channelValue, constantValue):
        if ((1 / channelValue) < constantValue):
            return 1 / channelValue;
        elif ((self.MIN_CONSTANT_VALUE / channelValue) > constantValue):
            return self.MIN_CONSTANT_VALUE / channelValue;
        else:
            return constantValue;


    # scenario 1
    def greenBlueConstant(self, color, dRL, cr):
        return (dRL - (0.2126 * color[0] * cr)) / ((0.7152 * color[1]) + (0.0722 * color[2]));

    # scenario 2
    def redBlueConstant(self, color, dRL, cg):
        return (dRL - (0.7152 * color[1] * cg)) / ((0.2126 * color[0]) + (0.0722 * color[2]));

    # scenario 3
    def redGreenConstant(self, color, dRL, cb):
        return (dRL - (0.0722 * color[2] * cb)) / ((0.2126 * color[0]) + (0.7152 * color[1]));

    # scenario 4
    def blueConstant(self, color, dRL, cr, cg):
        return (dRL - (0.2126 * color[0] * cr) - (0.7152 * color[1] * cg)) / (0.0722 * color[2]);

    # scenario 5
    def greenConstant(self, color, dRL, cr, cb):
        return (dRL - (0.2126 * color[0] * cr) - (0.0722 * color[2] * cb)) / (0.7152 * color[1]);

    # scenario 6
    def redConstant(self, color, dRL, cg, cb):
        return (dRL - (0.7152 * color[1] * cg) - (0.0722 * color[2] * cb)) / (0.2126 * color[0]);

    def desiredRelativeLuminance(self, contrast):
        return (1.05 / contrast) - 0.05;

    def currentRelativeLuminance(self, color):
        return (0.2126 * color[0]) + (0.7152 * color[1]) + (0.0722 * color[2]);

    def currentContrast(self, color):
        return 1.05 / (self.currentRelativeLuminance(color) + 0.05)

    def luminanceConstant(self, color, dRL):
        channelConstant = dRL / ((0.2126 * color[0]) + (0.7152 * color[1]) + (0.0722 * color[2]));

        return [
            channelConstant,
            channelConstant,
            channelConstant,
        ];

    def constant(self, color, contrast):
        currentContrast = self.currentContrast(color);
        desiredContrast = currentContrast - contrast
        if (desiredContrast < 0):
            desiredContrast = currentContrast + contrast
        if (desiredContrast >= 21):
            desiredContrast = 21.0
            
        dRL = self.desiredRelativeLuminance(desiredContrast);

        constant = self.luminanceConstant(color, dRL);
        minConstant = self.MinConstant(color);
        maxConstant = self.MaxConstant(color);

        if (Scenario().GreenBlue(constant, minConstant, maxConstant)):
            constant[1] = self.set(color[1], constant[1]);
            constant[2] = self.set(color[2], constant[2]);

            constant[0] = self.redConstant(color, dRL, constant[1], constant[2]);
        elif (Scenario().RedBlue(constant, minConstant, maxConstant)):
            constant[0] = self.set(color[0], constant[0]);
            constant[2] = self.set(color[2], constant[2]);

            constant[1] = self.greenConstant(color, dRL, constant[0], constant[2]);
        elif (Scenario().RedGreen(constant, minConstant, maxConstant)):
            constant[0] = self.set(color[0], constant[0]);
            constant[1] = self.set(color[1], constant[1]);
            
            constant[2] = self.blueConstant(color, dRL, constant[0], constant[1]);
        elif (Scenario().Blue(constant, minConstant, maxConstant)):
            constant[2] = self.set(color[2], constant[2]);
            
            constant[0] = self.redGreenConstant(color, dRL, constant[2]);
            constant[1] = constant[0];
        elif (Scenario().Green(constant, minConstant, maxConstant)):
            constant[1] = self.set(color[1], constant[1]);

            constant[0] = self.redBlueConstant(color, dRL, constant[1]);
            constant[2] = constant[0];
        elif (Scenario().Red(constant, minConstant, maxConstant)):
            constant[0] = self.set(color[0], constant[0]);

            constant[1] = self.greenBlueConstant(color, dRL, constant[0]);
            constant[2] = constant[1];


        return [
            constant[0],
            constant[1],
            constant[2],
        ]