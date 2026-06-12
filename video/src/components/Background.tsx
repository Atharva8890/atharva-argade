import React from "react";
import {
  AbsoluteFill,
  interpolate,
  Sequence,
  useCurrentFrame,
} from "remotion";
import { timeline } from "../lib/timeline";
import { Scene } from "../scenes/Scenes";
import { Footage, hasFootage } from "./Footage";

const FPS = timeline.fps;
const OVERLAP = Math.round(0.7 * FPS);

const FadeWrap: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const frame = useCurrentFrame();
  const op = interpolate(
    frame,
    [0, OVERLAP, dur - OVERLAP, dur],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return <AbsoluteFill style={{ opacity: op }}>{children}</AbsoluteFill>;
};

export const Background: React.FC = () => {
  const starts = timeline.chapters.map((c) => c.start);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {timeline.chapters.map((c, i) => {
        const nextStart = i + 1 < starts.length ? starts[i + 1] : timeline.totalSeconds;
        const from = Math.max(0, Math.round(c.start * FPS) - (i > 0 ? OVERLAP : 0));
        const to = Math.round(nextStart * FPS) + (i + 1 < starts.length ? OVERLAP : 0);
        const dur = Math.max(2, to - from);
        const fk = c.kind === "endcard" ? "endcard" : c.key;
        return (
          <Sequence key={i} from={from} durationInFrames={dur} layout="none">
            <FadeWrap dur={dur}>
              {hasFootage(fk) ? (
                <Footage chapterKey={fk} theme={c.theme} />
              ) : (
                <Scene scene={c.scene} theme={c.theme} seed={i + 1} dur={dur} />
              )}
            </FadeWrap>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
