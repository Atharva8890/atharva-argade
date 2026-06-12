import React from "react";
import {
  AbsoluteFill,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { timeline, sec } from "../lib/timeline";
import { anton, oswald } from "../theme";
import { withAlpha } from "../lib/sceneTypes";

const EndContent: React.FC<{ lines: string[]; accent: string; hold: number }> = ({
  lines,
  accent,
  hold,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fadeOut = interpolate(frame, [hold - 34, hold], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: fadeOut }}>
      <div style={{ textAlign: "center" }}>
        {lines.map((ln, i) => {
          const sp = spring({
            frame: frame - 10 - i * 18,
            fps,
            config: { damping: 200 },
            durationInFrames: 26,
          });
          const pulse = 1 + 0.015 * Math.sin((frame - i * 10) * 0.08);
          return (
            <div
              key={i}
              style={{
                fontFamily: anton,
                fontSize: 130,
                lineHeight: 1.05,
                letterSpacing: 3,
                color: "#fff",
                opacity: sp,
                transform: `translateY(${(1 - sp) * 40}px) scale(${sp * pulse})`,
                textShadow: `0 0 40px ${withAlpha(accent, 0.5)}, 0 12px 50px rgba(0,0,0,0.8)`,
              }}
            >
              {ln}
            </div>
          );
        })}
        <div
          style={{
            fontFamily: oswald,
            fontWeight: 500,
            letterSpacing: 10,
            fontSize: 24,
            color: accent,
            marginTop: 46,
            opacity: interpolate(frame, [70, 100], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          THE ART OF NEVER QUITTING
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const EndCard: React.FC = () => {
  const { fps } = useVideoConfig();
  const card = timeline.chapters.find((c) => c.kind === "endcard");
  if (!card) return null;
  const from = Math.round(sec(card.start));
  const dur = Math.round(sec(timeline.totalSeconds - card.start));
  const lines = card.title.split(".").map((s) => s.trim()).filter(Boolean);
  return (
    <Sequence from={from} durationInFrames={dur} layout="none">
      <EndContent lines={lines} accent={card.theme.accent} hold={dur} />
    </Sequence>
  );
};
