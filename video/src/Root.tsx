import React from "react";
import { Composition } from "remotion";
import { Documentary } from "./Documentary";
import { timeline } from "./lib/timeline";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Documentary"
      component={Documentary}
      durationInFrames={timeline.durationInFrames}
      fps={timeline.fps}
      width={timeline.width}
      height={timeline.height}
    />
  );
};
