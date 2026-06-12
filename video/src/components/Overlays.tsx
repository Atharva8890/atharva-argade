import React from "react";
import {
  AbsoluteFill,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { timeline, chapterAt, TOTAL_CHAPTERS } from "../lib/timeline";
import { oswald } from "../theme";
import { withAlpha } from "../lib/sceneTypes";

const pad2 = (n: number) => String(n).padStart(2, "0");

export const Letterbox: React.FC = () => (
  <>
    <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: "5.5%", background: "#000", zIndex: 60 }} />
    <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: "5.5%", background: "#000", zIndex: 60 }} />
  </>
);

export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(120% 100% at 50% 48%, transparent 52%, rgba(0,0,0,0.55) 100%)",
      pointerEvents: "none",
    }}
  />
);

// cheap GPU-friendly grain: a tiled noise PNG nudged every frame
const GRAIN = staticFile("img/grain.png");
export const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const tx = (frame * 13) % 160;
  const ty = (frame * 7) % 160;
  return (
    <AbsoluteFill
      style={{
        opacity: 0.08,
        mixBlendMode: "overlay",
        pointerEvents: "none",
        backgroundImage: `url(${GRAIN})`,
        backgroundRepeat: "repeat",
        backgroundSize: "160px 160px",
        backgroundPosition: `${tx}px ${ty}px`,
      }}
    />
  );
};

export const LightLeak: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / timeline.fps;
  const accent = chapterAt(t).theme.accent;
  const drift = Math.sin(frame * 0.01);
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "screen", opacity: 0.4 }}>
      <div
        style={{
          position: "absolute",
          top: "-20%",
          left: `${20 + drift * 25}%`,
          width: "60%",
          height: "60%",
          background: `radial-gradient(closest-side, ${withAlpha(accent, 0.18)}, transparent 70%)`,
          filter: "blur(30px)",
        }}
      />
    </AbsoluteFill>
  );
};

export const FilmHUD: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const ch = chapterAt(t);
  const prog = frame / durationInFrames;
  const showLabel = ch.kind === "chapter";
  const labelOp = showLabel
    ? interpolate(t - ch.start, [0.2, 0.8, 3.0, 3.6], [0, 0.55, 0.55, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 0;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 61 }}>
      {/* progress bar */}
      <div style={{ position: "absolute", bottom: "5.5%", left: 0, height: 3, width: `${prog * 100}%`, background: withAlpha(ch.theme.accent, 0.85) }} />
      <div style={{ position: "absolute", bottom: "5.5%", left: 0, right: 0, height: 3, background: "rgba(255,255,255,0.08)" }} />
      {/* chapter indicator */}
      <div
        style={{
          position: "absolute",
          bottom: "8%",
          left: "5%",
          fontFamily: oswald,
          fontWeight: 600,
          letterSpacing: 4,
          fontSize: 22,
          color: "#fff",
          opacity: labelOp,
        }}
      >
        <span style={{ color: ch.theme.accent }}>{pad2(ch.num)}</span>
        <span style={{ opacity: 0.5 }}> / {pad2(TOTAL_CHAPTERS)}</span>
        <span style={{ marginLeft: 14, opacity: 0.8 }}>{ch.title}</span>
      </div>
    </AbsoluteFill>
  );
};

export const Fades: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const open = interpolate(frame, [0, 22], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const close = interpolate(frame, [durationInFrames - 26, durationInFrames - 2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const op = Math.max(open, close);
  if (op <= 0) return null;
  return <AbsoluteFill style={{ background: "#000", opacity: op, zIndex: 70 }} />;
};

/* --------------------------- camera shake wrapper ----------------------- */
const BOOMS = timeline.chapters.filter((_, i) => i > 0).map((c) => c.start);

export const CameraShake: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  let kick = 0;
  for (const b of BOOMS) {
    const dt = t - b;
    if (dt >= 0 && dt < 0.5) kick = Math.max(kick, (1 - dt / 0.5) ** 2);
  }
  const x = Math.sin(frame * 0.08) * 2 + Math.sin(frame * 0.031) * 1.4 + Math.sin(frame * 0.5) * 6 * kick;
  const y = Math.cos(frame * 0.07) * 1.6 + Math.cos(frame * 0.6) * 5 * kick;
  const rot = Math.sin(frame * 0.02) * 0.15 + Math.sin(frame * 0.7) * 0.4 * kick;
  const scale = 1.035 + 0.03 * kick;
  return (
    <AbsoluteFill style={{ transform: `translate(${x}px,${y}px) rotate(${rot}deg) scale(${scale})`, transformOrigin: "50% 50%" }}>
      {children}
    </AbsoluteFill>
  );
};
