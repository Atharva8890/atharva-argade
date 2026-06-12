import React from "react";
import {
  AbsoluteFill,
  interpolate,
  random,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Theme, mix, withAlpha } from "../lib/sceneTypes";

/* ----------------------------------------------------------------------------
 * Original, fully procedural cinematic backdrops. No stock footage, no images.
 * Every scene reacts to the local Sequence frame (Ken Burns, parallax, drift).
 * ------------------------------------------------------------------------- */

const Sky: React.FC<{ theme: Theme; tilt?: number }> = ({ theme, tilt = 0 }) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(120% 90% at 50% ${110 - tilt}%, ${mix(
        theme.b,
        theme.accent,
        0.12
      )} 0%, ${theme.b} 32%, ${theme.a} 78%, #000 100%)`,
    }}
  />
);

/* -------------------------------- Starfield ----------------------------- */
export const Starfield: React.FC<{ theme: Theme; seed?: number; dur?: number }> = ({
  theme,
  seed = 1,
  dur,
}) => {
  const frame = useCurrentFrame();
  const cfg = useVideoConfig();
  const { width, height } = cfg;
  const durationInFrames = dur ?? cfg.durationInFrames;
  const stars = React.useMemo(
    () =>
      new Array(120).fill(0).map((_, i) => ({
        x: random(`x${seed}${i}`) * width,
        y: random(`y${seed}${i}`) * height,
        r: 0.6 + random(`r${seed}${i}`) * 2.2,
        sp: 0.15 + random(`s${seed}${i}`) * 0.6,
        ph: random(`p${seed}${i}`) * Math.PI * 2,
      })),
    [seed, width, height]
  );
  const drift = interpolate(frame, [0, durationInFrames], [0, -60]);
  return (
    <AbsoluteFill>
      <Sky theme={theme} />
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 50% at 30% 30%, ${withAlpha(
            theme.accent,
            0.12
          )} 0%, transparent 60%), radial-gradient(50% 45% at 75% 70%, ${withAlpha(
            mix(theme.accent, "#ffffff", 0.3),
            0.1
          )} 0%, transparent 60%)`,
        }}
      />
      {stars.map((s, i) => {
        const tw = 0.4 + 0.6 * Math.abs(Math.sin(frame * 0.05 * s.sp + s.ph));
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: s.x,
              top: (s.y + drift * s.sp + height) % height,
              width: s.r,
              height: s.r,
              borderRadius: "50%",
              background: "#fff",
              opacity: tw * 0.9,
              boxShadow: `0 0 ${s.r * 3}px ${withAlpha("#ffffff", 0.6)}`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

/* -------------------------------- Skyline ------------------------------- */
const buildingLayer = (
  seed: string,
  count: number,
  base: number,
  spread: number,
  width: number
) =>
  new Array(count).fill(0).map((_, i) => {
    const w = 60 + random(`w${seed}${i}`) * 130;
    return {
      x: (i / count) * width * 1.5 - width * 0.25 + random(`o${seed}${i}`) * 30,
      w,
      h: base + random(`h${seed}${i}`) * spread,
      lit: random(`l${seed}${i}`),
    };
  });

const BuildingRow: React.FC<{
  data: ReturnType<typeof buildingLayer>;
  color: string;
  win: string;
  speed: number;
  height: number;
}> = ({ data, color, win, speed, height }) => {
  const frame = useCurrentFrame();
  const dx = -((frame * speed) % 200);
  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height,
        transform: `translateX(${dx}px)`,
      }}
    >
      {data.map((b, i) => {
        const tw = 0.55 + 0.45 * Math.sin(frame * 0.06 + i * 1.7);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              bottom: 0,
              left: b.x,
              width: b.w,
              height: b.h,
              background: `linear-gradient(180deg, ${color} 0%, #000 100%)`,
              backgroundImage: `repeating-linear-gradient(180deg, transparent 0 11px, ${withAlpha(
                win,
                0.0
              )} 11px 12px), repeating-linear-gradient(90deg, transparent 0 14px, ${withAlpha(
                win,
                b.lit > 0.45 ? 0.5 * tw : 0.12
              )} 14px 17px), linear-gradient(180deg, ${color} 0%, #000 100%)`,
              borderTopLeftRadius: 2,
              borderTopRightRadius: 2,
              boxShadow: `0 0 40px ${withAlpha("#000", 0.6)}`,
            }}
          />
        );
      })}
    </div>
  );
};

export const Skyline: React.FC<{ theme: Theme; seed?: number; dur?: number }> = ({
  theme,
  seed = 1,
  dur,
}) => {
  const frame = useCurrentFrame();
  const cfg = useVideoConfig();
  const { width, height } = cfg;
  const durationInFrames = dur ?? cfg.durationInFrames;
  const kb = interpolate(frame, [0, durationInFrames], [1.05, 1.16]);
  const panY = interpolate(frame, [0, durationInFrames], [10, -26]);
  const far = React.useMemo(() => buildingLayer(`f${seed}`, 14, 220, 220, width), [seed, width]);
  const mid = React.useMemo(() => buildingLayer(`m${seed}`, 12, 320, 300, width), [seed, width]);
  const near = React.useMemo(() => buildingLayer(`n${seed}`, 9, 440, 360, width), [seed, width]);
  return (
    <AbsoluteFill>
      <Sky theme={theme} tilt={8} />
      {/* horizon glow */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(70% 40% at 50% 88%, ${withAlpha(
            theme.accent,
            0.28
          )} 0%, transparent 60%)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `scale(${kb}) translateY(${panY}px)`,
          transformOrigin: "50% 100%",
        }}
      >
        <BuildingRow data={far} color={mix(theme.b, "#000", 0.3)} win={theme.accent} speed={0.12} height={height} />
        <BuildingRow data={mid} color={mix(theme.a, "#000", 0.1)} win={mix(theme.accent, "#fff", 0.2)} speed={0.28} height={height} />
        <BuildingRow data={near} color="#04060a" win={theme.accent} speed={0.5} height={height} />
      </div>
      {/* atmospheric haze */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, transparent 40%, ${withAlpha(
            theme.a,
            0.5
          )} 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};

/* --------------------------------- Grid --------------------------------- */
export const Grid: React.FC<{ theme: Theme; seed?: number }> = ({ theme }) => {
  const frame = useCurrentFrame();
  const move = (frame * 0.6) % 80;
  return (
    <AbsoluteFill>
      <Sky theme={theme} />
      <AbsoluteFill style={{ perspective: 700, perspectiveOrigin: "50% 40%" }}>
        <div
          style={{
            position: "absolute",
            inset: "-40% -40%",
            transform: "rotateX(64deg)",
            backgroundImage: `linear-gradient(${withAlpha(theme.accent, 0.5)} 1px, transparent 1px), linear-gradient(90deg, ${withAlpha(
              theme.accent,
              0.5
            )} 1px, transparent 1px)`,
            backgroundSize: "80px 80px",
            backgroundPosition: `0px ${move}px`,
            maskImage:
              "radial-gradient(closest-side, #000 30%, transparent 80%)",
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 50% at 50% 42%, ${withAlpha(
            theme.accent,
            0.16
          )} 0%, transparent 60%)`,
        }}
      />
      {/* scan line */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: `${(frame * 0.4) % 100}%`,
          height: 2,
          background: withAlpha(theme.accent, 0.35),
          filter: "blur(1px)",
        }}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------- WorldMap ------------------------------ */
export const WorldMap: React.FC<{ theme: Theme; seed?: number; dur?: number }> = ({
  theme,
  dur,
}) => {
  const frame = useCurrentFrame();
  const cfg = useVideoConfig();
  const { width, height } = cfg;
  const durationInFrames = dur ?? cfg.durationInFrames;
  const rot = interpolate(frame, [0, durationInFrames], [0, 14]);
  const nodes = React.useMemo(
    () =>
      new Array(7).fill(0).map((_, i) => ({
        x: 0.2 * width + random(`mx${i}`) * 0.6 * width,
        y: 0.28 * height + random(`my${i}`) * 0.42 * height,
      })),
    [width, height]
  );
  const dots = React.useMemo(
    () =>
      new Array(420).fill(0).map((_, i) => ({
        x: random(`dx${i}`) * width,
        y: random(`dy${i}`) * height,
        on: random(`do${i}`) > 0.55,
      })),
    [width, height]
  );
  return (
    <AbsoluteFill>
      <Sky theme={theme} />
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `rotate(${rot * 0.05}deg) scale(${interpolate(
            frame,
            [0, durationInFrames],
            [1.04, 1.12]
          )})`,
        }}
      >
        {/* dot-matrix continents impression */}
        <svg width={width} height={height} style={{ position: "absolute" }}>
          {dots.map((d, i) => (
            <circle
              key={i}
              cx={d.x}
              cy={d.y}
              r={d.on ? 2.1 : 1.1}
              fill={withAlpha(theme.accent, d.on ? 0.6 : 0.18)}
            />
          ))}
          {nodes.map((n, i) => {
            const m = nodes[(i + 1) % nodes.length];
            const t = (frame * 0.9 + i * 24) % 120;
            const prog = Math.min(1, t / 80);
            const mx = (n.x + m.x) / 2;
            const my = (n.y + m.y) / 2 - 120;
            const path = `M ${n.x} ${n.y} Q ${mx} ${my} ${m.x} ${m.y}`;
            return (
              <g key={`a${i}`}>
                <path d={path} fill="none" stroke={withAlpha(theme.accent, 0.25)} strokeWidth={1.2} />
                <path
                  d={path}
                  fill="none"
                  stroke={mix(theme.accent, "#fff", 0.4)}
                  strokeWidth={2.4}
                  strokeDasharray="220"
                  strokeDashoffset={(1 - prog) * 220}
                  style={{ filter: `drop-shadow(0 0 6px ${theme.accent})` }}
                />
              </g>
            );
          })}
          {nodes.map((n, i) => {
            const pulse = 4 + 5 * Math.abs(Math.sin(frame * 0.08 + i));
            return (
              <g key={`n${i}`}>
                <circle cx={n.x} cy={n.y} r={pulse} fill="none" stroke={withAlpha(theme.accent, 0.4)} />
                <circle cx={n.x} cy={n.y} r={3.2} fill={mix(theme.accent, "#fff", 0.5)} />
              </g>
            );
          })}
        </svg>
      </div>
    </AbsoluteFill>
  );
};

/* -------------------------------- Flares -------------------------------- */
export const Flares: React.FC<{ theme: Theme; seed?: number }> = ({
  theme,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const x = width * (0.3 + 0.4 * (0.5 + 0.5 * Math.sin(frame * 0.012)));
  const y = height * (0.32 + 0.12 * Math.sin(frame * 0.017));
  const motes = React.useMemo(
    () =>
      new Array(40).fill(0).map((_, i) => ({
        x: random(`fx${i}`) * width,
        y: random(`fy${i}`) * height,
        r: 1 + random(`fr${i}`) * 3,
        sp: 0.2 + random(`fs${i}`) * 0.8,
      })),
    [width, height]
  );
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${theme.b}, ${theme.a} 70%, #000)` }}>
      {/* volumetric god-ray cone */}
      <div
        style={{
          position: "absolute",
          left: x,
          top: y,
          width: 4,
          height: 4,
          background: mix(theme.accent, "#fff", 0.4),
          borderRadius: "50%",
          boxShadow: `0 0 120px 60px ${withAlpha(theme.accent, 0.5)}, 0 0 320px 160px ${withAlpha(theme.accent, 0.18)}`,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: x - 600,
          top: y - 30,
          width: 1200,
          height: 60,
          background: `linear-gradient(90deg, transparent, ${withAlpha(theme.accent, 0.5)}, transparent)`,
          filter: "blur(6px)",
          transform: `rotate(${8 + 4 * Math.sin(frame * 0.02)}deg)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: x - 700,
          top: y - 700,
          width: 1400,
          height: 1400,
          transform: `rotate(${frame * 0.25}deg)`,
          background: `radial-gradient(closest-side, ${withAlpha(theme.accent, 0.12)}, transparent 70%)`,
          maskImage:
            "repeating-conic-gradient(#000 0deg 10deg, transparent 10deg 30deg)",
          opacity: 0.5,
        }}
      />
      {motes.map((m, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: m.x,
            top: (m.y - frame * m.sp + height) % height,
            width: m.r,
            height: m.r,
            borderRadius: "50%",
            background: withAlpha("#fff", 0.5),
            filter: "blur(0.5px)",
            opacity: 0.5,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

/* -------------------------------- Embers (Fall) ------------------------- */
export const Embers: React.FC<{ theme: Theme; seed?: number }> = ({
  theme,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const embers = React.useMemo(
    () =>
      new Array(70).fill(0).map((_, i) => ({
        x: random(`ex${i}`) * width,
        y: random(`ey${i}`) * height,
        r: 1 + random(`er${i}`) * 3,
        sp: 0.4 + random(`es${i}`) * 1.4,
        sway: random(`ew${i}`) * 40,
      })),
    [width, height]
  );
  return (
    <AbsoluteFill style={{ background: `radial-gradient(120% 100% at 50% 120%, ${mix(theme.b,"#000",0.1)} 0%, ${theme.a} 60%, #000 100%)` }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 50% at 50% 100%, ${withAlpha(theme.accent, 0.22)} 0%, transparent 60%)`,
        }}
      />
      {embers.map((e, i) => {
        const yy = (e.y - frame * e.sp + height) % height;
        const xx = e.x + Math.sin(frame * 0.03 + i) * e.sway;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: xx,
              top: yy,
              width: e.r,
              height: e.r,
              borderRadius: "50%",
              background: mix(theme.accent, "#fff", 0.2),
              boxShadow: `0 0 ${e.r * 4}px ${withAlpha(theme.accent, 0.8)}`,
              opacity: 0.7,
            }}
          />
        );
      })}
      {/* drifting smoke */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 30% at ${30 + 20 * Math.sin(frame * 0.01)}% 30%, ${withAlpha("#000", 0.5)} 0%, transparent 70%)`,
          mixBlendMode: "multiply",
        }}
      />
    </AbsoluteFill>
  );
};

export const Scene: React.FC<{ scene: string; theme: Theme; seed: number; dur?: number }> = ({
  scene,
  theme,
  seed,
  dur,
}) => {
  switch (scene) {
    case "skyline":
      return <Skyline theme={theme} seed={seed} dur={dur} />;
    case "grid":
      return <Grid theme={theme} seed={seed} />;
    case "map":
      return <WorldMap theme={theme} seed={seed} dur={dur} />;
    case "flare":
      return <Flares theme={theme} seed={seed} />;
    case "dark":
      return <Embers theme={theme} seed={seed} />;
    case "stars":
    default:
      return <Starfield theme={theme} seed={seed} dur={dur} />;
  }
};
