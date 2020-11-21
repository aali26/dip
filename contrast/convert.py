from contrast.calculate import Calculate
import numpy as np

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

    def image(self, image, contrast):
        # get all unique colors
        colors = np.unique(image.reshape(-1, image.shape[2]),axis=0)
        # get contrasts of all colors
        new_colors = [];
        for color in colors:
            contrast_color = self.transform(color / 256, contrast)
            new_colors.append((np.array(contrast_color) * 256).astype("uint8"));

        # convert each pixel of current image to use the new colors
        red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2]
        for i in range(0, len(colors)):
            color = colors[i];
            mask = (red == color[0]) & (green == color[1]) & (blue == color[2])
            image[:,:,:3][mask] = new_colors[i]

        return image;
