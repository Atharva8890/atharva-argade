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
import { Theme, mix, withAlpha } from "../lib/sceneTypes";

const pad2 = (n: number) => String(n).padStart(2, "0");

const ChapterCard: React.FC<{
  num: number;
  title: string;
  kicker: string;
  theme: Theme;
  hold: number;
}> = ({ num, title, kicker, theme, hold }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 22 });
  const exit = interpolate(frame, [hold - 16, hold], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const op = Math.min(enter, exit);
  const wipe = interpolate(enter, [0, 1], [0, 100]);
  const rule = interpolate(enter, [0, 1], [0, 1]);

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: op }}>
      <div style={{ position: "relative", textAlign: "center", padding: "0 6%" }}>
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "-58%",
            transform: `translateX(-50%) translateX(${(1 - enter) * 40}px)`,
            fontFamily: anton,
            fontSize: 360,
            lineHeight: 1,
            color: withAlpha(theme.accent, 0.1),
            letterSpacing: 4,
            pointerEvents: "none",
          }}
        >
          {pad2(num)}
        </div>
        <div
          style={{
            fontFamily: oswald,
            fontWeight: 600,
            letterSpacing: 10,
            fontSize: 24,
            color: theme.accent,
            marginBottom: 14,
            transform: `translateY(${(1 - enter) * 14}px)`,
          }}
        >
          CHAPTER {pad2(num)}
        </div>
        <div
          style={{
            fontFamily: anton,
            fontSize: 116,
            lineHeight: 0.98,
            color: "#fff",
            letterSpacing: 2,
            textShadow: "0 8px 40px rgba(0,0,0,0.7)",
            clipPath: `inset(0 ${100 - wipe}% 0 0)`,
          }}
        >
          {title}
        </div>
        <div
          style={{
            height: 3,
            width: 220,
            margin: "22px auto 0",
            background: `linear-gradient(90deg, transparent, ${theme.accent}, transparent)`,
            transform: `scaleX(${rule})`,
          }}
        />
        {kicker ? (
          <div
            style={{
              fontFamily: oswald,
              fontWeight: 500,
              letterSpacing: 6,
              fontSize: 26,
              color: "rgba(255,255,255,0.7)",
              marginTop: 18,
              textTransform: "uppercase",
              opacity: enter,
            }}
          >
            {kicker}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

const TitleSequence: React.FC<{ title: string; kicker: string; theme: Theme; hold: number }> = ({
  title,
  kicker,
  theme,
  hold,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 30 });
  const exit = interpolate(frame, [hold - 22, hold], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const op = Math.min(enter, exit);
  const words = title.split(" ");
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: op }}>
      <div style={{ textAlign: "center", padding: "0 6%" }}>
        <div
          style={{
            fontFamily: oswald,
            fontWeight: 600,
            letterSpacing: 14,
            fontSize: 22,
            color: theme.accent,
            marginBottom: 26,
            opacity: enter,
            transform: `translateY(${(1 - enter) * 12}px)`,
          }}
        >
          A MOTIVATIONAL DOCUMENTARY
        </div>
        <div style={{ fontFamily: anton, fontSize: 150, lineHeight: 0.95, color: "#fff", letterSpacing: 2 }}>
          {words.map((w, i) => {
            const wp = spring({ frame: frame - i * 4, fps, config: { damping: 200 }, durationInFrames: 24 });
            return (
              <span
                key={i}
                style={{
                  display: "inline-block",
                  margin: "0 0.18em",
                  opacity: wp,
                  transform: `translateY(${(1 - wp) * 40}px) scale(${0.9 + wp * 0.1})`,
                  textShadow: "0 10px 50px rgba(0,0,0,0.8)",
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
        <div
          style={{
            height: 3,
            width: 360,
            margin: "30px auto 0",
            background: `linear-gradient(90deg, transparent, ${theme.accent}, transparent)`,
            transform: `scaleX(${enter})`,
          }}
        />
        <div
          style={{
            fontFamily: oswald,
            fontWeight: 400,
            letterSpacing: 5,
            fontSize: 28,
            color: "rgba(255,255,255,0.72)",
            marginTop: 22,
            textTransform: "uppercase",
            opacity: interpolate(frame, [16, 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          }}
        >
          {kicker}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const ChapterTitles: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      {timeline.chapters.map((c, i) => {
        if (c.kind === "chapter") {
          const hold = Math.round(3.4 * fps);
          const from = Math.round(sec((c.cardAt ?? c.start) - 0.15));
          return (
            <Sequence key={i} from={from} durationInFrames={hold} layout="none">
              <ChapterCard num={c.num} title={c.title} kicker={c.kicker} theme={c.theme} hold={hold} />
            </Sequence>
          );
        }
        if (c.kind === "title") {
          const hold = Math.round(5.0 * fps);
          const from = Math.round(sec(c.start));
          return (
            <Sequence key={i} from={from} durationInFrames={hold} layout="none">
              <TitleSequence title={c.title} kicker={c.kicker} theme={c.theme} hold={hold} />
            </Sequence>
          );
        }
        return null;
      })}
    </>
  );
};
