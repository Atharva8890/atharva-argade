import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadOswald } from "@remotion/google-fonts/Oswald";

const fontOpts = { subsets: ["latin"], ignoreTooManyRequestsWarning: true } as const;

export const anton = loadAnton("normal", { ...fontOpts, weights: ["400"] }).fontFamily;
export const inter = loadInter("normal", { ...fontOpts, weights: ["400", "800"] }).fontFamily;
export const oswald = loadOswald("normal", { ...fontOpts, weights: ["500", "600"] }).fontFamily;

export const INK = "#f6f4ee";
export const SUB = "rgba(246,244,238,0.55)";

export { mix, withAlpha } from "./lib/sceneTypes";
