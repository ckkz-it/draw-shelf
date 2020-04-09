type RGB = { r: number; g: number; b: number };

/*
  https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
 */
const hexToRgb = (hex: string): RGB => {
  // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
  const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
  hex = hex.replace(shorthandRegex, (_, r, g, b) => {
    return r + r + g + g + b + b;
  });

  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16),
  };
};

const rgbStringToObject = (rgbColor: string): RGB => {
  const regExp = /^rgb\(([\d]+)[\s]*,[\s]*([\d]+)[\s]*,[\s]*([\d]+).*\)$/i;
  const result = regExp.exec(rgbColor);
  return {
    r: parseInt(result[1], 10),
    g: parseInt(result[2], 10),
    b: parseInt(result[3], 10),
  };
};

export const getTextColorBasedOnBg = (
  color: string,
  hex = true,
  blackColor = 'black',
  whiteColor = 'white',
) => {
  let rgbColor: RGB;
  if (hex) {
    rgbColor = hexToRgb(color);
  } else {
    rgbColor = rgbStringToObject(color);
  }
  // YIQ formula
  const brightness = Math.round((rgbColor.r * 299 + rgbColor.g * 587 + rgbColor.b * 114) / 1000);
  return brightness > 128 ? blackColor : whiteColor;
};
