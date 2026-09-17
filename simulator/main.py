import asyncio
import random
from typing import List
from rich.console import Console
from rich.table import Table
from rich.live import Live

import config
from models import Asset, Gateway, Location, Telemetry
from movement import update_asset
from ble import generate_telemetry

def generate_random_location() -> Location:
    lat = random.uniform(config.CAMPUS_BOUNDS["min_lat"], config.CAMPUS_BOUNDS["max_lat"])
    lng = random.uniform(config.CAMPUS_BOUNDS["min_lng"], config.CAMPUS_BOUNDS["max_lng"])
    return Location(lat=lat, lng=lng)

def init_gateways() -> List[Gateway]:
    gateways = []
    zones = ["Main Hall", "Engineering Block", "Labs", "Library", "Admin Block"]
    for i in range(config.NUM_GATEWAYS):
        gw = Gateway(
            gateway_id=f"GW-{i+1:02d}",
            name=f"Gateway {zones[i % len(zones)]}",
            location=generate_random_location(),
            zone=zones[i % len(zones)]
        )
        gateways.append(gw)
    return gateways

def init_assets() -> List[Asset]:
    assets = []
    for i in range(config.NUM_ASSETS):
        category = random.choice(config.ASSET_CATEGORIES)
        # Generate 3-5 random waypoints for this asset
        num_waypoints = random.randint(3, 5)
        waypoints = [generate_random_location() for _ in range(num_waypoints)]
        
        asset = Asset(
            asset_id=f"AST-{i+1:03d}",
            name=f"Asset-{i+1:03d}",
            category=category,
            location=Location(lat=waypoints[0].lat, lng=waypoints[0].lng),
            battery=random.uniform(80.0, 100.0),
            status=config.ASSET_STATUS_ONLINE,
            waypoints=waypoints,
            current_waypoint_index=1 % len(waypoints)
        )
        assets.append(asset)
    return assets

def generate_table(telemetry_list: List[Telemetry]) -> Table:
    """Generate a rich table for terminal output."""
    table = Table(title="Campus Asset Tracker - Simulated IoT Environment", show_header=True, header_style="bold magenta")
    
    table.add_column("Asset ID", style="cyan", width=10)
    table.add_column("Category", width=15)
    table.add_column("Location (Lat, Lng)", justify="right", width=25)
    table.add_column("Gateway", style="green", width=10)
    table.add_column("RSSI", justify="right", width=10)
    table.add_column("Battery", justify="right", width=10)
    table.add_column("Status", width=10)

    for t in telemetry_list:
        battery_color = "green" if t.battery > 50 else "yellow" if t.battery > 20 else "red"
        status_color = "green" if t.status == "online" else "grey50"
        
        table.add_row(
            t.asset_id,
            t.category,
            f"{t.lat:.6f}, {t.lng:.6f}",
            t.gateway_id,
            f"{t.rssi:.1f} dBm",
            f"[{battery_color}]{t.battery:.1f}%[/{battery_color}]",
            f"[{status_color}]{t.status}[/{status_color}]"
        )
        
    return table

async def main():
    if config.RANDOM_SEED is not None:
        random.seed(config.RANDOM_SEED)

    console = Console()
    console.print("[bold green]Starting Simulator...[/bold green]")
    
    gateways = init_gateways()
    assets = init_assets()
    
    try:
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                telemetry_data = []
                
                for asset in assets:
                    # Update position and battery
                    update_asset(asset, config.SIMULATION_INTERVAL_SEC)
                    
                    # Generate telemetry (simulate BLE broadcast + gateway reception)
                    telemetry = generate_telemetry(asset, gateways)
                    telemetry_data.append(telemetry)
                
                # Update terminal UI
                table = generate_table(telemetry_data)
                live.update(table)
                
                # Wait for next tick
                await asyncio.sleep(config.SIMULATION_INTERVAL_SEC)
                
    except KeyboardInterrupt:
        console.print("[bold red]Simulator stopped.[/bold red]")

if __name__ == "__main__":
    asyncio.run(main())
