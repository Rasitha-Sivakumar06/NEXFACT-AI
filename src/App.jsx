import { useState } from "react";
import "./App.css";

const machines = [
  {
    id: "M01",
    health: "MONITOR",
    energy: "0.000104",
    utilization: "100.0%",
    abnormal: 0,
    power: "4.52",
    temperature: "43.8",
    vibration: "1.93",
    rpm: "1460",
    production: "29",
  },
  {
    id: "M02",
    health: "HIGH_RISK",
    energy: "0.000097",
    utilization: "0.0%",
    abnormal: 12,
    power: "6.71",
    temperature: "63.9",
    vibration: "4.71",
    rpm: "1242",
    production: "12",
  },
  {
    id: "M03",
    health: "NORMAL",
    energy: "0.000186",
    utilization: "28.6%",
    abnormal: 0,
    power: "4.31",
    temperature: "41.8",
    vibration: "1.43",
    rpm: "1471",
    production: "23",
  },
];

const orders = [
  {
    id: "ORD001",
    product: "Component-A",
    quantity: 500,
    priority: "HIGH",
    machine: "M01",
    time: "1.67 h",
    energy: "0.0521",
    score: "71.96",
  },
  {
    id: "ORD002",
    product: "Component-B",
    quantity: 700,
    priority: "MEDIUM",
    machine: "M01",
    time: "2.33 h",
    energy: "0.0729",
    score: "60.30",
  },
  {
    id: "ORD003",
    product: "Component-C",
    quantity: 400,
    priority: "LOW",
    machine: "M03",
    time: "1.14 h",
    energy: "0.0745",
    score: "64.29",
  },
];

const totalPlannedUnits = orders.reduce(
  (sum, order) => sum + order.quantity,
  0
);
const totalEnergyDemand = orders.reduce(
  (sum, order) => sum + Number(order.energy),
  0
);
const averageEnergyPerUnit = totalEnergyDemand / totalPlannedUnits;
const bestEnergyMachine = [...machines].sort(
  (a, b) => Number(a.energy) - Number(b.energy)
)[0];
const productionOptimizationInsights = [
  {
    title: "Best energy fit",
    value: bestEnergyMachine.id,
    detail: "Lowest energy intensity asset available",
    tone: "good",
  },
  {
    title: "Energy per unit",
    value: `${averageEnergyPerUnit.toFixed(4)} kWh`,
    detail: "Across all scheduled production",
    tone: "neutral",
  },
  {
    title: "Production output",
    value: `${totalPlannedUnits.toLocaleString()} units`,
    detail: "Current factory load target",
    tone: "good",
  },
  {
    title: "Optimization gain",
    value: "+18.4%",
    detail: "Potential reduction in energy intensity",
    tone: "highlight",
  },
];

function App() {
  const [activePage, setActivePage] = useState("Overview");
  const [selectedMachine, setSelectedMachine] = useState("M02");

  const activeMachine =
    machines.find((machine) => machine.id === selectedMachine) || machines[0];

  const navigation = [
    {
      section: "COMMAND CENTER",
      items: [
        { name: "Overview", icon: "⌂" },
      ],
    },
    {
      section: "MACHINE INTELLIGENCE",
      items: [
        { name: "Machine Health", icon: "◉" },
        { name: "Live Telemetry", icon: "⌁" },
        { name: "Anomaly Detection", icon: "△" },
      ],
    },
    {
      section: "ENERGY INTELLIGENCE",
      items: [
        { name: "Energy Analytics", icon: "ϟ" },
        { name: "Efficiency", icon: "◈" },
      ],
    },
    {
      section: "PRODUCTION AI",
      items: [
        { name: "Production Plan", icon: "▤" },
        { name: "Scheduler", icon: "◫" },
        { name: "Optimization", icon: "◎" },
      ],
    },
    {
      section: "IMPACT",
      items: [
        { name: "Energy Impact", icon: "◌" },
        { name: "CO₂ & Cost", icon: "◍" },
      ],
    },
  ];

  const renderPageContent = () => {
    if (activePage === "Overview") {
      return <Overview />;
    }

    if (activePage === "Machine Health") {
      return (
        <MachineHealth
          machines={machines}
          selectedMachine={selectedMachine}
          setSelectedMachine={setSelectedMachine}
        />
      );
    }

    if (activePage === "Live Telemetry") {
      return <Telemetry machine={activeMachine} />;
    }

    if (activePage === "Anomaly Detection") {
      return <AnomalyDetection />;
    }

    if (
      activePage === "Energy Analytics" ||
      activePage === "Efficiency"
    ) {
      return <EnergyAnalytics />;
    }

    if (
      activePage === "Production Plan" ||
      activePage === "Scheduler" ||
      activePage === "Optimization"
    ) {
      return <ProductionAI />;
    }

    if (
      activePage === "Energy Impact" ||
      activePage === "CO₂ & Cost"
    ) {
      return <ImpactAnalysis />;
    }

    return <Overview />;
  };

  return (
    <div className="app-shell">
      <div className="background-grid"></div>
      <div className="ambient ambient-one"></div>
      <div className="ambient ambient-two"></div>
      <div className="ambient ambient-three"></div>

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <span>N</span>
          </div>

          <div>
            <div className="brand-name">NEXFACT</div>
            <div className="brand-ai">AI</div>
          </div>
        </div>

        <div className="brand-subtitle">
          INDUSTRIAL INTELLIGENCE
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          <span>SYSTEM ONLINE</span>
        </div>

        <nav className="navigation">
          {navigation.map((group) => (
            <div className="nav-group" key={group.section}>
              <div className="nav-section-title">{group.section}</div>

              {group.items.map((item) => (
                <button
                  key={item.name}
                  className={`nav-item ${
                    activePage === item.name ? "active" : ""
                  }`}
                  onClick={() => setActivePage(item.name)}
                >
                  <span className="nav-icon">{item.icon}</span>
                  <span>{item.name}</span>

                  {activePage === item.name && (
                    <span className="nav-active-line"></span>
                  )}
                </button>
              ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="simulation-chip">
            <span className="pulse-small"></span>
            SIMULATION MODE
          </div>

          <div className="version">
            NEXFACT AI v1.0
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="breadcrumb">
              NEXFACT AI <span>/</span> {activePage}
            </div>

            <h1>{activePage}</h1>
          </div>

          <div className="topbar-right">
            <div className="factory-status">
              <span className="status-dot"></span>
              ALL SYSTEMS OPERATIONAL
            </div>

            <div className="clock">
              <span>29 SEP 2026</span>
              <strong>09:43 AM</strong>
            </div>
          </div>
        </header>

        {renderPageContent()}
      </main>
    </div>
  );
}

function Overview() {
  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <div className="eyebrow">
            <span></span>
            AI FACTORY OPERATIONS PLATFORM
          </div>

          <div className="hero-factory-tag">AI FACTORY</div>

          <h2>
            <span className="ai-brain-highlight">The AI brain</span>
            <br />
            <span>of your plant.</span>
          </h2>

          <p>
            Smart factory intelligence for machine health, energy
            optimization, production planning and autonomous plant
            decision support — unified by NEXFACT AI.
          </p>

          <div className="hero-actions">
            <button className="primary-button">
              <span>EXPLORE FACTORY</span>
              <span>→</span>
            </button>

            <button className="secondary-button">
              VIEW LIVE TELEMETRY
            </button>
          </div>
        </div>

        <FactoryVisualization />
      </section>

      <section className="metric-grid">
        <MetricCard
          label="MACHINES MONITORED"
          value="03"
          suffix="ASSETS"
          icon="◉"
          detail="Factory assets connected"
        />

        <MetricCard
          label="PLANNED PRODUCTION"
          value="1,600"
          suffix="UNITS"
          icon="▤"
          detail="Production scheduled"
        />

        <MetricCard
          label="PRODUCTION ENERGY"
          value="0.1995"
          suffix="KWH"
          icon="ϟ"
          detail="Estimated consumption"
        />

        <MetricCard
          label="HIGH-RISK MACHINES"
          value="01"
          suffix="ALERT"
          icon="!"
          danger
          detail="M02 excluded"
        />
      </section>

      <section className="section-block">
        <div className="section-heading">
          <div>
            <div className="section-kicker">AI SAFETY LAYER</div>
            <h3>Autonomous Safety Decision</h3>
          </div>

          <span className="live-badge">
            <span></span>
            LIVE
          </span>
        </div>

        <div className="safety-card">
          <div className="safety-icon">
            !
          </div>

          <div className="safety-main">
            <div className="safety-title">
              MACHINE M02 — HIGH RISK
            </div>

            <p>
              NEXFACT AI detected <strong>12 abnormal events</strong>
              {" "}across power consumption, temperature, vibration,
              RPM and production output.
            </p>

            <div className="safety-tags">
              <span>12 ABNORMAL EVENTS</span>
              <span>HIGH RISK</span>
              <span>PRODUCTION BLOCKED</span>
            </div>
          </div>

          <button className="outline-button">
            VIEW ANALYSIS →
          </button>
        </div>
      </section>

      <section className="section-block">
        <div className="section-heading">
          <div>
            <div className="section-kicker">LIVE INTELLIGENCE</div>
            <h3>Machine Command Center</h3>
          </div>

          <span className="updated">
            ● Updated from factory telemetry
          </span>
        </div>

        <div className="machine-grid">
          {machines.map((machine) => (
            <MachineCard
              key={machine.id}
              machine={machine}
            />
          ))}
        </div>
      </section>

      <section className="section-block">
        <div className="section-heading">
          <div>
            <div className="section-kicker">AI DECISION ENGINE</div>
            <h3>Production Allocation</h3>
          </div>

          <span className="optimized-badge">
            MULTI-OBJECTIVE OPTIMIZED
          </span>
        </div>

        <ProductionTable />
      </section>

      <section className="bottom-grid">
        <div className="glass-panel energy-panel">
          <div className="section-kicker">ENERGY INTELLIGENCE</div>
          <h3>Energy Impact</h3>

          <div className="energy-orb">
            <div className="orb-core">ϟ</div>
          </div>

          <div className="energy-number">
            0.1995 <span>kWh</span>
          </div>

          <p>Estimated production energy</p>

          <div className="energy-stats">
            <div>
              <span>ELECTRICITY COST</span>
              <strong>₹1.60</strong>
            </div>

            <div>
              <span>CO₂ EMISSIONS</span>
              <strong>0.1396 kg</strong>
            </div>
          </div>
        </div>

        <div className="glass-panel pipeline-panel">
          <div className="section-kicker">COPILOT STATUS</div>
          <h3>Decision Pipeline</h3>

          <div className="pipeline">
            {[
              "Factory data analyzed",
              "Machine health evaluated",
              "Anomalies detected",
              "Production optimized",
              "Energy impact estimated",
            ].map((item, index) => (
              <div className="pipeline-item" key={item}>
                <div className="pipeline-number">
                  {String(index + 1).padStart(2, "0")}
                </div>

                <div className="pipeline-line"></div>

                <div className="pipeline-check">
                  ✓
                </div>

                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="footer">
        <div>
          <strong>NEXFACT AI</strong>
          <span>Industrial decision support system</span>
        </div>

        <span>
          PROTOTYPE • SIMULATED INDUSTRIAL TELEMETRY
        </span>
      </footer>
    </>
  );
}

function FactoryVisualization() {
  return (
    <div className="factory-stage">
      <div className="stage-grid"></div>

      <div className="stage-label label-top">
        DIGITAL FACTORY TWIN
      </div>

      <div className="factory-floor">
        <div className="floor-ring ring-one"></div>
        <div className="floor-ring ring-two"></div>

        <FactoryMachine
          id="M01"
          x="20%"
          y="43%"
          health="MONITOR"
        />

        <FactoryMachine
          id="M02"
          x="50%"
          y="28%"
          health="HIGH_RISK"
          danger
        />

        <FactoryMachine
          id="M03"
          x="76%"
          y="50%"
          health="NORMAL"
        />

        <div className="connection connection-one"></div>
        <div className="connection connection-two"></div>
        <div className="connection connection-three"></div>

        <div className="factory-core">
          <div className="core-ring"></div>
          <div className="core-logo">N</div>
          <span>NEXFACT</span>
        </div>
      </div>

      <div className="telemetry-chip chip-one">
        <span>POWER</span>
        <strong>4.52 kW</strong>
      </div>

      <div className="telemetry-chip chip-two">
        <span>PRODUCTION</span>
        <strong>1,600</strong>
      </div>

      <div className="telemetry-chip chip-three">
        <span>EFFICIENCY</span>
        <strong>94.2%</strong>
      </div>

      <div className="scan-line"></div>
    </div>
  );
}

function FactoryMachine({ id, x, y, health, danger }) {
  return (
    <div
      className={`factory-machine ${danger ? "danger" : ""}`}
      style={{ left: x, top: y }}
    >
      <div className="machine-pulse"></div>
      <div className="machine-core">
        <div className="machine-inner"></div>
      </div>

      <div className="machine-label">
        <strong>{id}</strong>
        <span>{health}</span>
      </div>
    </div>
  );
}

function MetricCard({
  label,
  value,
  suffix,
  icon,
  detail,
  danger,
}) {
  return (
    <div className={`metric-card ${danger ? "danger-card" : ""}`}>
      <div className="metric-top">
        <span>{label}</span>
        <div className="metric-icon">{icon}</div>
      </div>

      <div className="metric-value">
        {value}
        <small>{suffix}</small>
      </div>

      <div className="metric-detail">
        <span className="tiny-dot"></span>
        {detail}
      </div>
    </div>
  );
}

function MachineCard({ machine }) {
  const isDanger = machine.health === "HIGH_RISK";

  return (
    <div className={`machine-card ${isDanger ? "machine-danger" : ""}`}>
      <div className="machine-card-top">
        <div>
          <div className="machine-id">{machine.id}</div>

          <div
            className={`health-status ${
              isDanger
                ? "health-danger"
                : machine.health === "MONITOR"
                ? "health-monitor"
                : "health-normal"
            }`}
          >
            <span></span>
            {machine.health}
          </div>
        </div>

        <div className="machine-visual">
          <div className="machine-visual-ring"></div>
          <div className="machine-visual-core">
            {machine.id.replace("M", "")}
          </div>
        </div>
      </div>

      <div className="machine-stat-row">
        <div>
          <span>ENERGY / UNIT</span>
          <strong>{machine.energy}</strong>
          <small>kWh/unit</small>
        </div>

        <div>
          <span>UTILIZATION</span>
          <strong>{machine.utilization}</strong>
        </div>
      </div>

      <div className="machine-bottom">
        <div className="mini-stat">
          <span>ABNORMAL EVENTS</span>
          <strong className={isDanger ? "red-text" : ""}>
            {machine.abnormal}
          </strong>
        </div>

        <div className="mini-stat">
          <span>POWER</span>
          <strong>{machine.power} kW</strong>
        </div>
      </div>
    </div>
  );
}

function ProductionTable() {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>ORDER</th>
            <th>PRODUCT</th>
            <th>QUANTITY</th>
            <th>PRIORITY</th>
            <th>MACHINE</th>
            <th>TIME</th>
            <th>ENERGY</th>
            <th>SCORE</th>
          </tr>
        </thead>

        <tbody>
          {orders.map((order) => (
            <tr key={order.id}>
              <td className="order-id">{order.id}</td>
              <td>{order.product}</td>
              <td>{order.quantity} units</td>
              <td>
                <span
                  className={`priority priority-${order.priority.toLowerCase()}`}
                >
                  {order.priority}
                </span>
              </td>
              <td>
                <span className="machine-pill">
                  {order.machine}
                </span>
              </td>
              <td>{order.time}</td>
              <td>{order.energy} kWh</td>
              <td>
                <strong className="score">{order.score}</strong>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MachineHealth({
  machines,
  selectedMachine,
  setSelectedMachine,
}) {
  return (
    <div className="page-content">
      <div className="page-intro">
        <div>
          <div className="section-kicker">MACHINE INTELLIGENCE</div>
          <h2>Machine Health</h2>
          <p>
            Real-time health classification based on simulated
            industrial telemetry.
          </p>
        </div>

        <div className="large-status">
          <span></span>
          3 MACHINES ONLINE
        </div>
      </div>

      <div className="machine-health-grid">
        {machines.map((machine) => (
          <button
            key={machine.id}
            className={`health-large-card ${
              selectedMachine === machine.id ? "selected" : ""
            }`}
            onClick={() => setSelectedMachine(machine.id)}
          >
            <div className="large-machine-orb">
              <div>{machine.id.replace("M", "")}</div>
            </div>

            <h3>{machine.id}</h3>

            <div
              className={`health-status ${
                machine.health === "HIGH_RISK"
                  ? "health-danger"
                  : machine.health === "MONITOR"
                  ? "health-monitor"
                  : "health-normal"
              }`}
            >
              <span></span>
              {machine.health}
            </div>

            <div className="health-large-stats">
              <div>
                <span>POWER</span>
                <strong>{machine.power} kW</strong>
              </div>

              <div>
                <span>TEMP</span>
                <strong>{machine.temperature}°C</strong>
              </div>

              <div>
                <span>VIBRATION</span>
                <strong>{machine.vibration}</strong>
              </div>

              <div>
                <span>RPM</span>
                <strong>{machine.rpm}</strong>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

function Telemetry({ machine }) {
  return (
    <div className="page-content">
      <div className="page-intro">
        <div>
          <div className="section-kicker">LIVE TELEMETRY</div>
          <h2>{machine.id} Telemetry</h2>
          <p>
            Streaming industrial sensor values from the simulated
            factory environment.
          </p>
        </div>

        <div className="large-status">
          <span></span>
          LIVE STREAM
        </div>
      </div>

      <div className="telemetry-grid">
        <TelemetryCard
          label="POWER CONSUMPTION"
          value={machine.power}
          unit="kW"
          percentage={72}
        />

        <TelemetryCard
          label="TEMPERATURE"
          value={machine.temperature}
          unit="°C"
          percentage={64}
        />

        <TelemetryCard
          label="VIBRATION"
          value={machine.vibration}
          unit="mm/s"
          percentage={48}
        />

        <TelemetryCard
          label="ROTATIONAL SPEED"
          value={machine.rpm}
          unit="RPM"
          percentage={82}
        />
      </div>

      <div className="glass-panel telemetry-chart">
        <div className="section-kicker">TELEMETRY HISTORY</div>
        <h3>Sensor Activity</h3>

        <div className="chart">
          <div className="chart-grid"></div>

          <div className="chart-line">
            {Array.from({ length: 22 }).map((_, index) => (
              <span
                key={index}
                style={{
                  height: `${25 + ((index * 17) % 55)}%`,
                }}
              ></span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function TelemetryCard({
  label,
  value,
  unit,
  percentage,
}) {
  return (
    <div className="telemetry-card">
      <div className="telemetry-card-top">
        <span>{label}</span>
        <span className="live-dot"></span>
      </div>

      <div className="telemetry-value">
        {value}
        <small>{unit}</small>
      </div>

      <div className="progress-track">
        <div
          className="progress-value"
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
}

function AnomalyDetection() {
  return (
    <div className="page-content">
      <div className="page-intro">
        <div>
          <div className="section-kicker">AI SAFETY ENGINE</div>
          <h2>Anomaly Detection</h2>
          <p>
            NEXFACT AI detected abnormal machine behavior from
            factory telemetry.
          </p>
        </div>

        <div className="alert-count">
          12 ACTIVE EVENTS
        </div>
      </div>

      <div className="anomaly-hero">
        <div className="anomaly-ring">
          <span>12</span>
          <small>EVENTS</small>
        </div>

        <div>
          <div className="section-kicker">PRIMARY ALERT</div>
          <h3>M02 — HIGH RISK CONDITION</h3>
          <p>
            Power, temperature and vibration increased while RPM
            and production output decreased.
          </p>

          <div className="anomaly-tags">
            <span>POWER ↑</span>
            <span>TEMP ↑</span>
            <span>VIBRATION ↑</span>
            <span>RPM ↓</span>
            <span>OUTPUT ↓</span>
          </div>
        </div>
      </div>

      <div className="anomaly-list">
        {[5, 4, 4, 4, 4, 3].map((score, index) => (
          <div className="anomaly-row" key={index}>
            <div className="anomaly-time">
              09:42:{40 + index * 2}
            </div>

            <div>
              <strong>M02</strong>
              <span>ABNORMAL MACHINE STATE</span>
            </div>

            <div className="anomaly-score">
              SCORE {score}/5
            </div>

            <div
              className={`risk ${
                score >= 4 ? "risk-high" : "risk-medium"
              }`}
            >
              {score >= 4 ? "HIGH" : "MEDIUM"}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function EnergyAnalytics() {
  return (
    <div className="page-content">
      <div className="page-intro">
        <div>
          <div className="section-kicker">ENERGY INTELLIGENCE</div>
          <h2>Energy Analytics</h2>
          <p>
            Energy consumption and production efficiency across
            monitored machines.
          </p>
        </div>

        <div className="large-status">
          <span></span>
          ENERGY ENGINE ONLINE
        </div>
      </div>

      <div className="energy-dashboard">
        <div className="energy-big-card">
          <div className="section-kicker">TOTAL OBSERVED ENERGY</div>

          <div className="big-energy">
            0.2239
            <small>kWh</small>
          </div>

          <p>Across monitored machine telemetry</p>

          <div className="energy-wave">
            {Array.from({ length: 30 }).map((_, i) => (
              <span
                key={i}
                style={{
                  height: `${20 + ((i * 23) % 70)}%`,
                }}
              ></span>
            ))}
          </div>
        </div>

        <div className="efficiency-card">
          <div className="section-kicker">EFFICIENCY RANKING</div>
          <h3>Energy / Production Unit</h3>

          <EfficiencyRow
            machine="M02"
            value="0.000097"
            width="92%"
          />

          <EfficiencyRow
            machine="M01"
            value="0.000104"
            width="84%"
          />

          <EfficiencyRow
            machine="M03"
            value="0.000186"
            width="51%"
          />
        </div>
      </div>

      <div className="energy-metrics">
        <MetricCard
          label="ELECTRICITY COST"
          value="₹1.60"
          suffix="EST."
          icon="₹"
          detail="Current production plan"
        />

        <MetricCard
          label="CO₂ EMISSIONS"
          value="0.1396"
          suffix="KG"
          icon="CO₂"
          detail="Estimated footprint"
        />

        <MetricCard
          label="BEST INTENSITY"
          value="M02"
          suffix="MACHINE"
          icon="◈"
          detail="Observed efficiency"
        />
      </div>
    </div>
  );
}

function EfficiencyRow({ machine, value, width }) {
  return (
    <div className="efficiency-row">
      <div className="efficiency-label">
        <strong>{machine}</strong>
        <span>{value} kWh/unit</span>
      </div>

      <div className="efficiency-bar">
        <div style={{ width }}></div>
      </div>
    </div>
  );
}

function ProductionAI() {
  const recommendedShift = {
    order: "ORD002",
    from: "M01",
    to: bestEnergyMachine.id,
    gain: "18.4%",
    reason: "Flexible production batch can move to the most efficient healthy asset.",
  };

  return (
    <div className="page-content">
      <div className="page-intro">
        <div>
          <div className="section-kicker">PRODUCTION AI</div>
          <h2>Production Optimization</h2>
          <p>
            Multi-objective production planning balancing machine
            health, energy and capacity.
          </p>
        </div>

        <div className="optimized-badge">
          AI OPTIMIZED
        </div>
      </div>

      <div className="energy-production-overview">
        <div className="section-kicker">ENERGY + PRODUCTION OPTIMIZATION</div>
        <h3>Integrated efficiency model</h3>

        <div className="optimization-metric-grid">
          {productionOptimizationInsights.map((insight) => (
            <div
              key={insight.title}
              className={`optimization-metric tone-${insight.tone}`}
            >
              <span>{insight.title}</span>
              <strong>{insight.value}</strong>
              <small>{insight.detail}</small>
            </div>
          ))}
        </div>
      </div>

      <ProductionTable />

      <div className="schedule-grid">
        <div className="glass-panel">
          <div className="section-kicker">MACHINE UTILIZATION</div>
          <h3>Factory Workload</h3>

          <ScheduleBar
            machine="M01"
            workload="4.00 h"
            utilization="100%"
            width="100%"
          />

          <ScheduleBar
            machine="M02"
            workload="0.00 h"
            utilization="0%"
            width="0%"
            danger
          />

          <ScheduleBar
            machine="M03"
            workload="1.14 h"
            utilization="28.6%"
            width="28.6%"
          />
        </div>

        <div className="glass-panel decision-card">
          <div className="section-kicker">AI DECISION</div>

          <div className="decision-score">
            <span>AVERAGE SCORE</span>
            <strong>65.52</strong>
            <small>/100</small>
          </div>

          <p>
            High-risk assets are automatically excluded while
            production capacity and energy intensity are considered.
          </p>

          <div className="recommendation-box">
            <span className="recommendation-tag">RECOMMENDATION</span>
            <strong>
              {recommendedShift.order} move: {recommendedShift.from} → {recommendedShift.to}
            </strong>
            <small>
              {recommendedShift.reason}
            </small>
          </div>

          <button className="primary-button full">
            VIEW FINAL SCHEDULE →
          </button>
        </div>
      </div>
    </div>
  );
}

function ScheduleBar({
  machine,
  workload,
  utilization,
  width,
  danger,
}) {
  return (
    <div className="schedule-row">
      <div className="schedule-label">
        <strong>{machine}</strong>
        <span>{workload}</span>
        <span>{utilization}</span>
      </div>

      <div className="schedule-track">
        <div
          className={danger ? "schedule-fill danger-fill" : "schedule-fill"}
          style={{ width }}
        ></div>
      </div>
    </div>
  );
}

function ImpactAnalysis() {
  const savingsSummary = [
    {
      label: "MONTHLY ENERGY SAVINGS",
      value: "₹245",
      unit: "/ month",
      tone: "good",
    },
    {
      label: "ANNUAL SAVINGS",
      value: "₹2,947",
      unit: "/ year",
      tone: "highlight",
    },
    {
      label: "CO₂ REDUCTION",
      value: "0.025",
      unit: "tCO₂e",
      tone: "neutral",
    },
    {
      label: "PAYBACK PERIOD",
      value: "2.8",
      unit: "months",
      tone: "good",
    },
  ];

  return (
    <div className="page-content">
      <div className="page-intro">
        <div>
          <div className="section-kicker">FACTORY IMPACT</div>
          <h2>Energy & Environmental Impact</h2>
          <p>
            Estimated operational impact of the AI-generated
            production schedule.
          </p>
        </div>

        <div className="large-status">
          <span></span>
          IMPACT ENGINE ONLINE
        </div>
      </div>

      <div className="impact-grid">
        <ImpactCard
          label="PRODUCTION ENERGY"
          value="0.1995"
          unit="kWh"
          icon="ϟ"
        />

        <ImpactCard
          label="ELECTRICITY COST"
          value="₹1.60"
          unit="EST."
          icon="₹"
        />

        <ImpactCard
          label="CO₂ EMISSIONS"
          value="0.1396"
          unit="kg"
          icon="CO₂"
        />
      </div>

      <div className="glass-panel savings-panel">
        <div className="section-kicker">FINANCIAL OPTIMIZATION</div>
        <h3>Projected savings from AI scheduling</h3>

        <div className="savings-grid">
          {savingsSummary.map((item) => (
            <div
              key={item.label}
              className={`savings-card tone-${item.tone}`}
            >
              <span>{item.label}</span>
              <strong>{item.value}</strong>
              <small>{item.unit}</small>
            </div>
          ))}
        </div>
      </div>

      <div className="glass-panel impact-explanation">
        <div className="section-kicker">
          NEXFACT DECISION REASONING
        </div>

        <h3>Why M02 was excluded</h3>

        <div className="reason-grid">
          <Reason
            number="01"
            title="ABNORMAL BEHAVIOR"
            text="12 abnormal telemetry events detected."
          />

          <Reason
            number="02"
            title="THERMAL STRESS"
            text="Temperature repeatedly exceeded the normal operating range."
          />

          <Reason
            number="03"
            title="VIBRATION"
            text="Vibration increased significantly during abnormal operation."
          />

          <Reason
            number="04"
            title="PRODUCTION LOSS"
            text="Production output dropped while energy consumption increased."
          />
        </div>
      </div>
    </div>
  );
}

function ImpactCard({ label, value, unit, icon }) {
  return (
    <div className="impact-card">
      <div className="impact-icon">{icon}</div>

      <span>{label}</span>

      <strong>
        {value}
        <small>{unit}</small>
      </strong>

      <div className="impact-line"></div>
    </div>
  );
}

function Reason({ number, title, text }) {
  return (
    <div className="reason">
      <div className="reason-number">{number}</div>

      <div>
        <strong>{title}</strong>
        <p>{text}</p>
      </div>
    </div>
  );
}

export default App;