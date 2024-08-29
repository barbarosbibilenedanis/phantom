import { cn } from "../utils/phantomUtils";
import React from "react";

const Skeleton = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(function Skeleton({ className, ...props }, ref) {
  return (
    <div
      ref={ref}
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  );
});

export { Skeleton };
