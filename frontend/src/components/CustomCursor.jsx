import { useEffect, useRef, useState } from "react";

const LERP_FACTOR = 0.18;

function hasFinePointer() {
  return typeof window !== "undefined" && window.matchMedia("(pointer: fine)").matches;
}

export default function CustomCursor() {
  const [enabled] = useState(hasFinePointer);
  const dotRef = useRef(null);
  const target = useRef({ x: -100, y: -100 });
  const current = useRef({ x: -100, y: -100 });
  const hovering = useRef(false);
  const currentScale = useRef(1);
  const rafId = useRef(null);

  useEffect(() => {
    if (!enabled) return;

    function handleMouseMove(e) {
      target.current.x = e.clientX;
      target.current.y = e.clientY;
    }

    function handleOver(e) {
      if (e.target.closest("a, button")) {
        hovering.current = true;
      }
    }

    function handleOut(e) {
      if (e.target.closest("a, button")) {
        hovering.current = false;
      }
    }

    function tick() {
      current.current.x += (target.current.x - current.current.x) * LERP_FACTOR;
      current.current.y += (target.current.y - current.current.y) * LERP_FACTOR;
      const targetScale = hovering.current ? 0.1 : 1;
      currentScale.current += (targetScale - currentScale.current) * LERP_FACTOR;
      if (dotRef.current) {
        dotRef.current.style.transform = `translate3d(${current.current.x - 16}px, ${current.current.y - 16}px, 0) scale(${currentScale.current})`;
      }
      rafId.current = requestAnimationFrame(tick);
    }

    window.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseover", handleOver);
    document.addEventListener("mouseout", handleOut);
    rafId.current = requestAnimationFrame(tick);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseover", handleOver);
      document.removeEventListener("mouseout", handleOut);
      if (rafId.current) cancelAnimationFrame(rafId.current);
    };
  }, [enabled]);

  if (!enabled) return null;

  return <div ref={dotRef} className="custom-cursor" aria-hidden="true" />;
}
