/**
 * Enterprise Sales & Revenue Intelligence - Live Client Application
 * Handles data filtering, KPI computations, Chart.js rendering, and interactive UI
 */

let masterData = null;
let currentTab = 'rp01';
let chartMonthly = null;
let chartRegional = null;
let chartCategory = null;
let chartSegments = null;

// Initialize app
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("data.json");
    masterData = await res.json();
    renderAll();
  } catch (err) {
    console.error("Failed to load data.json:", err);
  }
});

function formatCurrency(val) {
  if (val === undefined || val === null || isNaN(val)) return "$0.00";
  return "$" + Number(val).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatNumber(val) {
  if (val === undefined || val === null || isNaN(val)) return "0";
  return Number(val).toLocaleString("en-US");
}

function switchTab(tabId) {
  currentTab = tabId;
  document.querySelectorAll(".tab-content").forEach(el => el.classList.add("hidden"));
  const activeContent = document.getElementById(`tab-${tabId}`);
  if (activeContent) activeContent.classList.remove("hidden");

  // Update nav buttons
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.remove("text-blue-400", "border-blue-500");
    btn.classList.add("text-slate-400", "border-transparent");
  });
  const activeBtn = document.getElementById(`nav-${tabId}`);
  if (activeBtn) {
    activeBtn.classList.add("text-blue-400", "border-blue-500");
    activeBtn.classList.remove("text-slate-400", "border-transparent");
  }

  // Trigger chart resize / re-render if needed
  if (tabId === 'rp01') {
    if (chartMonthly) chartMonthly.resize();
    if (chartRegional) chartRegional.resize();
    if (chartCategory) chartCategory.resize();
  } else if (tabId === 'rp04') {
    if (chartSegments) chartSegments.resize();
  }
}

function applyFilters() {
  renderAll();
}

function resetFilters() {
  document.getElementById("filter-year").value = "All";
  document.getElementById("filter-region").value = "All";
  document.getElementById("filter-category").value = "All";
  applyFilters();
}

function getFilteredData() {
  if (!masterData) return null;

  const selYear = document.getElementById("filter-year").value;
  const selRegion = document.getElementById("filter-region").value;
  const selCategory = document.getElementById("filter-category").value;

  // Update badge
  const badge = document.getElementById("active-filter-badge");
  badge.textContent = `Context: Year=${selYear} | Region=${selRegion} | Cat=${selCategory}`;

  // Filter Monthly records
  let filteredMonthly = masterData.monthly.filter(row => {
    const yearMatch = (selYear === "All") || row.YearMonth.startsWith(selYear);
    const regMatch = (selRegion === "All") || (row.Region === selRegion);
    const catMatch = (selCategory === "All") || (row.Category === selCategory);
    return yearMatch && regMatch && catMatch;
  });

  // Filter Targets records
  let filteredTargets = masterData.targets.filter(row => {
    const yearMatch = (selYear === "All") || row.YearMonth.startsWith(selYear);
    const regMatch = (selRegion === "All") || (row.Region === selRegion);
    return yearMatch && regMatch;
  });

  // Recalculate summary metrics
  let totalRev = 0, totalGross = 0, totalDisc = 0, totalCOGS = 0, totalProf = 0, totalUnits = 0, totalOrders = 0;
  filteredMonthly.forEach(r => {
    totalRev += r.Revenue;
    totalGross += r.GrossSales;
    totalDisc += (r.GrossSales - r.Revenue);
    totalCOGS += r.COGS;
    totalProf += r.Profit;
    totalUnits += r.Units;
    totalOrders += r.Orders;
  });

  let totalTargetRev = 0;
  filteredTargets.forEach(t => {
    totalTargetRev += t.RevenueTarget;
  });

  // When category is filtered, adjust target proportionally
  if (selCategory !== "All" && masterData.summary.netRevenue > 0) {
    const catProportion = totalRev / masterData.summary.netRevenue;
    totalTargetRev = totalTargetRev * catProportion;
  }

  const marginPct = totalRev > 0 ? (totalProf / totalRev * 100) : 0;
  const aov = totalOrders > 0 ? (totalRev / totalOrders) : 0;
  const attainmentPct = totalTargetRev > 0 ? (totalRev / totalTargetRev * 100) : 0;

  return {
    summary: {
      netRevenue: totalRev,
      grossSales: totalGross,
      discounts: totalDisc,
      cogs: totalCOGS,
      grossProfit: totalProf,
      marginPct: marginPct,
      orders: totalOrders,
      units: totalUnits,
      aov: aov,
      targetRevenue: totalTargetRev,
      attainmentPct: attainmentPct
    },
    monthly: filteredMonthly,
    targets: filteredTargets,
    selYear,
    selRegion,
    selCategory
  };
}

function renderAll() {
  const data = getFilteredData();
  if (!data) return;

  renderKPICards(data.summary);
  renderCharts(data);
  renderSalespersonTable(data);
  renderProductTables(data);
  renderSegmentView(data);
  renderWaterfall(data.summary);
  renderTransactions(data);
}

function renderKPICards(s) {
  document.getElementById("kpi-revenue").textContent = formatCurrency(s.netRevenue);
  document.getElementById("kpi-profit").textContent = formatCurrency(s.grossProfit);
  document.getElementById("kpi-margin").textContent = `Margin: ${s.marginPct.toFixed(1)}%`;
  document.getElementById("kpi-margin-pct").textContent = `${s.marginPct.toFixed(1)}%`;
  document.getElementById("kpi-orders").textContent = formatNumber(s.orders);
  document.getElementById("kpi-units").textContent = `Units: ${formatNumber(s.units)}`;
  document.getElementById("kpi-aov").textContent = formatCurrency(s.aov);
  document.getElementById("kpi-attainment").textContent = `${s.attainmentPct.toFixed(1)}%`;

  const statusEl = document.getElementById("kpi-target-status");
  if (s.attainmentPct >= 105) {
    statusEl.textContent = "🟢 Overachieved (>105%)";
    statusEl.className = "text-[11px] text-emerald-600 font-medium mt-0.5";
  } else if (s.attainmentPct >= 95) {
    statusEl.textContent = "🟢 On Track (95-105%)";
    statusEl.className = "text-[11px] text-emerald-600 font-medium mt-0.5";
  } else if (s.attainmentPct >= 85) {
    statusEl.textContent = "🟡 At Risk (85-94%)";
    statusEl.className = "text-[11px] text-amber-600 font-medium mt-0.5";
  } else {
    statusEl.textContent = "🔴 Behind Target (<85%)";
    statusEl.className = "text-[11px] text-rose-600 font-medium mt-0.5";
  }
}

function renderCharts(d) {
  // Aggregate Monthly Time Series
  const monthMap = {};
  d.monthly.forEach(r => {
    monthMap[r.YearMonth] = (monthMap[r.YearMonth] || 0) + r.Revenue;
  });

  const targetMap = {};
  d.targets.forEach(t => {
    targetMap[t.YearMonth] = (targetMap[t.YearMonth] || 0) + t.RevenueTarget;
  });

  const months = Object.keys(monthMap).sort();
  const revSeries = months.map(m => monthMap[m]);
  const targetSeries = months.map(m => targetMap[m] || null);

  // 1. Monthly Trend Chart
  const ctxTrend = document.getElementById("chart-monthly-trend").getContext("2d");
  if (chartMonthly) chartMonthly.destroy();
  chartMonthly = new Chart(ctxTrend, {
    type: "line",
    data: {
      labels: months,
      datasets: [
        {
          label: "Actual Net Revenue ($)",
          data: revSeries,
          borderColor: "#2563eb",
          backgroundColor: "rgba(37, 99, 235, 0.1)",
          borderWidth: 2,
          fill: true,
          tension: 0.3
        },
        {
          label: "Target Quota ($)",
          data: targetSeries,
          borderColor: "#f59e0b",
          borderDash: [5, 5],
          borderWidth: 2,
          fill: false,
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top", labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${formatCurrency(ctx.parsed.y)}`
          }
        }
      },
      scales: {
        y: {
          ticks: {
            callback: (v) => "$" + (v / 1e6).toFixed(1) + "M",
            font: { size: 10 }
          },
          grid: { color: "#f1f5f9" }
        },
        x: {
          ticks: { font: { size: 9 }, maxRotation: 45 },
          grid: { display: false }
        }
      }
    }
  });

  // 2. Regional Breakdown
  const regMap = {};
  d.monthly.forEach(r => {
    regMap[r.Region] = (regMap[r.Region] || 0) + r.Revenue;
  });
  const regLabels = Object.keys(regMap);
  const regValues = regLabels.map(l => regMap[l]);

  const ctxReg = document.getElementById("chart-regional").getContext("2d");
  if (chartRegional) chartRegional.destroy();
  chartRegional = new Chart(ctxReg, {
    type: "doughnut",
    data: {
      labels: regLabels,
      datasets: [{
        data: regValues,
        backgroundColor: ["#1e3a8a", "#0d9488", "#f59e0b", "#64748b"]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 10, font: { size: 11 } } }
      }
    }
  });

  // 3. Category Breakdown
  const catMap = {};
  d.monthly.forEach(r => {
    catMap[r.Category] = (catMap[r.Category] || 0) + r.Revenue;
  });
  const catLabels = Object.keys(catMap);
  const catValues = catLabels.map(l => catMap[l]);

  const ctxCat = document.getElementById("chart-category").getContext("2d");
  if (chartCategory) chartCategory.destroy();
  chartCategory = new Chart(ctxCat, {
    type: "bar",
    data: {
      labels: catLabels,
      datasets: [{
        label: "Net Revenue ($)",
        data: catValues,
        backgroundColor: "#0d9488",
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          ticks: { callback: (v) => "$" + (v / 1e6).toFixed(1) + "M", font: { size: 10 } },
          grid: { color: "#f1f5f9" }
        },
        x: { ticks: { font: { size: 10 } }, grid: { display: false } }
      }
    }
  });
}

function renderProductTables(d) {
  let products = masterData.products;
  if (d.selCategory !== "All") {
    products = products.filter(p => p.Category === d.selCategory);
  }

  // Top 5 Products
  const topBody = document.getElementById("top-products-table");
  topBody.innerHTML = "";
  products.slice(0, 5).forEach(p => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="py-2 font-medium text-slate-800">${p.ProductName}</td>
      <td class="py-2 text-slate-500">${p.Category}</td>
      <td class="py-2 text-right font-semibold text-slate-900">${formatCurrency(p.Revenue)}</td>
      <td class="py-2 text-right font-medium text-emerald-600">${p.MarginPct}%</td>
    `;
    topBody.appendChild(tr);
  });

  // Full Catalog in RP-03
  const fullBody = document.getElementById("full-product-table");
  fullBody.innerHTML = "";
  products.forEach(p => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-mono text-slate-500">${p.ProductID || 'PROD'}</td>
      <td class="py-2.5 px-3 font-medium text-slate-800">${p.ProductName}</td>
      <td class="py-2.5 px-3 text-slate-500">${p.Category}</td>
      <td class="py-2.5 px-3 text-right text-slate-600">${formatNumber(p.Units)}</td>
      <td class="py-2.5 px-3 text-right font-semibold text-slate-900">${formatCurrency(p.Revenue)}</td>
      <td class="py-2.5 px-3 text-right text-slate-700">${formatCurrency(p.Profit)}</td>
      <td class="py-2.5 px-3 text-right font-bold text-emerald-600">${p.MarginPct}%</td>
    `;
    fullBody.appendChild(tr);
  });
}

function renderSalespersonTable(d) {
  let reps = masterData.salespersons;
  if (d.selRegion !== "All") {
    reps = reps.filter(r => r.Region === d.selRegion);
  }

  const tbody = document.getElementById("salesperson-table");
  tbody.innerHTML = "";

  reps.forEach(r => {
    const variance = r.Revenue - r.TargetRevenue;
    const isExceeded = r.AttainmentPct >= 100;
    const statusBadge = isExceeded
      ? `<span class="px-2 py-0.5 rounded text-emerald-700 bg-emerald-50 border border-emerald-200 font-medium">🟢 Exceeded</span>`
      : (r.AttainmentPct >= 85
        ? `<span class="px-2 py-0.5 rounded text-amber-700 bg-amber-50 border border-amber-200 font-medium">🟡 On Track</span>`
        : `<span class="px-2 py-0.5 rounded text-rose-700 bg-rose-50 border border-rose-200 font-medium">🔴 Behind</span>`);

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-medium text-slate-800">${r.SalespersonName}</td>
      <td class="py-2.5 px-3 text-slate-500">${r.Region}</td>
      <td class="py-2.5 px-3 text-right font-semibold text-slate-900">${formatCurrency(r.Revenue)}</td>
      <td class="py-2.5 px-3 text-right text-slate-600">${formatCurrency(r.TargetRevenue)}</td>
      <td class="py-2.5 px-3 text-right font-medium ${variance >= 0 ? 'text-emerald-600' : 'text-rose-600'}">
        ${variance >= 0 ? '+' : ''}${formatCurrency(variance)}
      </td>
      <td class="py-2.5 px-3 text-center font-bold text-slate-800">${r.AttainmentPct}%</td>
      <td class="py-2.5 px-3 text-center">${statusBadge}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderSegmentView(d) {
  const segs = masterData.segments;
  const tbody = document.getElementById("segment-table");
  tbody.innerHTML = "";

  const labels = [];
  const revs = [];

  segs.forEach(s => {
    labels.push(s.Segment);
    revs.push(s.Revenue);

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="py-2 font-medium text-slate-800">${s.Segment}</td>
      <td class="py-2 text-right text-slate-600">${formatNumber(s.Customers)}</td>
      <td class="py-2 text-right text-slate-600">${formatNumber(s.Orders)}</td>
      <td class="py-2 text-right font-semibold text-slate-900">${formatCurrency(s.Revenue)}</td>
      <td class="py-2 text-right text-emerald-600 font-medium">${formatCurrency(s.Profit)}</td>
    `;
    tbody.appendChild(tr);
  });

  const ctxSeg = document.getElementById("chart-segments").getContext("2d");
  if (chartSegments) chartSegments.destroy();
  chartSegments = new Chart(ctxSeg, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Segment Revenue ($)",
        data: revs,
        backgroundColor: "#2563eb",
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { ticks: { callback: (v) => "$" + (v / 1e6).toFixed(1) + "M" } },
        x: { ticks: { font: { size: 10 } } }
      }
    }
  });
}

function renderWaterfall(s) {
  document.getElementById("wf-gross").textContent = formatCurrency(s.grossSales);
  document.getElementById("wf-disc").textContent = formatCurrency(s.discounts);
  const discRate = s.grossSales > 0 ? (s.discounts / s.grossSales * 100).toFixed(1) : 0;
  document.getElementById("wf-disc-pct").textContent = `${discRate}% Rate`;

  document.getElementById("wf-net").textContent = formatCurrency(s.netRevenue);
  document.getElementById("wf-cogs").textContent = formatCurrency(s.cogs);
  const costRatio = s.netRevenue > 0 ? (s.cogs / s.netRevenue * 100).toFixed(1) : 0;
  document.getElementById("wf-cogs-pct").textContent = `${costRatio}% Cost Basis`;

  document.getElementById("wf-profit").textContent = formatCurrency(s.grossProfit);
  document.getElementById("wf-margin-pct").textContent = `${s.marginPct.toFixed(1)}% Margin`;
}

function renderTransactions(d) {
  const tbody = document.getElementById("transaction-table");
  tbody.innerHTML = "";

  const txs = masterData.recentTransactions;
  txs.forEach(t => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-mono text-slate-500">${t.OrderLineID}</td>
      <td class="py-2.5 px-3 font-mono font-medium text-blue-600">${t.OrderID}</td>
      <td class="py-2.5 px-3 text-slate-500">${t.OrderDate}</td>
      <td class="py-2.5 px-3 font-medium text-slate-800">${t.CustomerName}</td>
      <td class="py-2.5 px-3 text-slate-700">${t.ProductName}</td>
      <td class="py-2.5 px-3 text-slate-500">${t.Region}</td>
      <td class="py-2.5 px-3 text-right text-slate-600">${t.Quantity}</td>
      <td class="py-2.5 px-3 text-right font-semibold text-slate-900">${formatCurrency(t.NetRevenue)}</td>
      <td class="py-2.5 px-3 text-right font-medium text-emerald-600">${formatCurrency(t.GrossProfit)}</td>
    `;
    tbody.appendChild(tr);
  });
}

function filterTransactions() {
  const query = document.getElementById("tx-search").value.toLowerCase();
  const rows = document.querySelectorAll("#transaction-table tr");
  rows.forEach(r => {
    const text = r.textContent.toLowerCase();
    r.style.display = text.includes(query) ? "" : "none";
  });
}

function exportTxToCSV() {
  if (!masterData || !masterData.recentTransactions) return;
  const headers = ["OrderLineID", "OrderID", "OrderDate", "CustomerName", "ProductName", "Category", "SalespersonName", "Region", "Quantity", "UnitPrice", "DiscountAmount", "NetRevenue", "GrossProfit"];
  const csvRows = [headers.join(",")];

  masterData.recentTransactions.forEach(t => {
    const row = headers.map(h => `"${t[h] !== undefined ? t[h] : ''}"`);
    csvRows.push(row.join(","));
  });

  const blob = new Blob([csvRows.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", `Enterprise_Sales_Transactions_${new Date().toISOString().slice(0,10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
