"use client";
import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { CitationNode } from "@/lib/api";

interface CitationGraphProps {
  nodes: CitationNode[];
  edges: { source: string; target: string }[];
}

export default function CitationGraph({ nodes, edges }: CitationGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || nodes.length === 0) return;

    const width = svgRef.current.clientWidth || 800;
    const height = 500;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    const g = svg.append("g");

    svg.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.3, 3])
        .on("zoom", (event) => g.attr("transform", event.transform))
    );

    const simulation = d3.forceSimulation(nodes as any)
      .force("link", d3.forceLink(edges).id((d: any) => d.id).distance(80))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide(30));

    const link = g.append("g")
      .selectAll("line")
      .data(edges)
      .enter().append("line")
      .attr("stroke", "#334155")
      .attr("stroke-width", 1.5)
      .attr("stroke-opacity", 0.6);

    const colorScale = d3.scaleSequential(d3.interpolateBlues)
      .domain([0, d3.max(nodes, (d) => d.citations) || 100]);

    const node = g.append("g")
      .selectAll("g")
      .data(nodes)
      .enter().append("g")
      .call(
        d3.drag<SVGGElement, CitationNode>()
          .on("start", (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
          })
          .on("drag", (event, d: any) => { d.fx = event.x; d.fy = event.y; })
          .on("end", (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
          })
      );

    node.append("circle")
      .attr("r", (d) => Math.max(6, Math.min(20, 6 + Math.sqrt(d.citations || 0) * 0.5)))
      .attr("fill", (d) => colorScale(d.citations || 0))
      .attr("stroke", "#60a5fa")
      .attr("stroke-width", 1.5)
      .attr("opacity", 0.85);

    node.append("text")
      .text((d) => d.title.length > 25 ? d.title.substring(0, 25) + "…" : d.title)
      .attr("x", 0)
      .attr("y", (d) => -Math.max(8, Math.min(22, 8 + Math.sqrt(d.citations || 0) * 0.5)) - 4)
      .attr("text-anchor", "middle")
      .attr("font-size", "9px")
      .attr("fill", "#94a3b8");

    node.append("title")
      .text((d) => `${d.title}\nYear: ${d.year || "N/A"}\nCitations: ${d.citations}`);

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    });

    return () => { simulation.stop(); };
  }, [nodes, edges]);

  return (
    <div className="w-full bg-slate-900 rounded-xl border border-slate-700 overflow-hidden">
      <svg ref={svgRef} className="w-full" style={{ height: "500px" }} />
      <div className="px-4 py-2 border-t border-slate-700 flex items-center gap-4 text-xs text-slate-500">
        <span>🔵 Larger = more citations</span>
        <span>Scroll to zoom • Drag to pan • Drag nodes to rearrange</span>
      </div>
    </div>
  );
}
