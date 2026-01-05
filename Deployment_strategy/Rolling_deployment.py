#!/usr/bin/env python3
"""
ROLLING DEPLOYMENT STRATEGY (Default/Progressive)

Purpose: Update pods one-by-one with zero downtime
         Maintains service availability during update

Key Parameters:
- maxSurge: Maximum extra pods allowed during update (can be number or percentage)
- maxUnavailable: Maximum unavailable pods during update (can be number or percentage)
"""

import time
from typing import List
from dataclasses import dataclass
from enum import Enum

# ========== DATA STRUCTURES ==========
class PodStatus(Enum):
    RUNNING = "running"
    TERMINATED = "terminated"
    PENDING = "pending"

@dataclass
class Pod:
    id: str
    version: str
    status: PodStatus
    is_ready: bool
    
    def __str__(self):
        return f"Pod-{self.id} (v{self.version}, {self.status.value})"

# ========== ROLLING DEPLOYMENT CLASS ==========
class RollingDeployment:
    """
    Simulates a Rolling Update Deployment Strategy
    
    How it works:
    1. Create new pod(s) (respecting maxSurge limit)
    2. Wait for new pod(s) to be ready
    3. Terminate old pod(s) (respecting maxUnavailable limit)
    4. Repeat until all pods are updated
    
    Key benefits:
    - Zero downtime
    - Progressive rollout
    - Automatic rollback if new pods fail
    """
    
    def __init__(self, app_name: str, initial_version: str = "1.0"):
        self.app_name = app_name
        self.current_version = initial_version
        self.new_version = None
        self.pods = []
        self.replica_count = 0
    
    def initialize_deployment(self, replica_count: int = 5):
        """Initialize deployment with specified number of replicas"""
        print(f"🔧 Initializing {self.app_name} deployment with {replica_count} pods")
        self.replica_count = replica_count
        self.pods = []
        
        for i in range(replica_count):
            pod = Pod(
                id=f"{self.app_name}-{i:03d}",
                version=self.current_version,
                status=PodStatus.RUNNING,
                is_ready=True
            )
            self.pods.append(pod)
        
        self.display_state("Initial Deployment")
    
    def rolling_update(self, new_version: str, max_surge: int = 1, max_unavailable: int = 1):
        """
        Execute rolling update
        
        Args:
            new_version: Version to deploy
            max_surge: Maximum extra pods allowed during update (absolute number)
            max_unavailable: Maximum unavailable pods allowed (absolute number)
        """
        print(f"\n🚀 STARTING ROLLING UPDATE")
        print(f"   Current: v{self.current_version}")
        print(f"   Target:  v{new_version}")
        print(f"   Strategy: maxSurge={max_surge}, maxUnavailable={max_unavailable}")
        print("=" * 60)
        
        self.new_version = new_version
        step = 1
        
        while True:
            print(f"\n📊 STEP {step}:")
            
            # Get current state
            old_pods = self._get_running_pods_by_version(self.current_version)
            new_pods = self._get_running_pods_by_version(new_version)
            all_running = self._get_running_pods()
            
            print(f"   Old pods running: {len(old_pods)}")
            print(f"   New pods running: {len(new_pods)}")
            print(f"   Total running: {len(all_running)}/{self.replica_count}")
            
            # Check if update is complete
            if len(old_pods) == 0 and len(new_pods) >= self.replica_count:
                print("\n✅ UPDATE COMPLETE!")
                self.current_version = new_version
                break
            
            # Calculate available pods
            available_pods = len(all_running)
            
            # Check maxUnavailable constraint
            if available_pods < self.replica_count - max_unavailable:
                print(f"   ⏳ Waiting: Only {available_pods} pods available")
                print(f"   Need at least {self.replica_count - max_unavailable} available")
                time.sleep(2)
                step += 1
                continue
            
            # Check if we can create new pods (maxSurge constraint)
            max_total_pods = self.replica_count + max_surge
            if len(all_running) < max_total_pods and len(new_pods) < self.replica_count:
                # Create new pod
                print(f"   ➕ Creating new pod (v{new_version})")
                self._create_new_pod(new_version)
            
            # Terminate old pod if we have enough new pods running
            if len(old_pods) > 0:
                # Check if we have capacity to terminate
                if available_pods - 1 >= self.replica_count - max_unavailable:
                    print(f"   ➖ Terminating old pod")
                    self._terminate_old_pod(old_pods[0])
                else:
                    print(f"   ⏳ Waiting: Can't terminate, would violate maxUnavailable")
            
            self.display_state(f"Step {step} Complete")
            time.sleep(2)
            step += 1
        
        self.display_state("Final State")
    
    def rolling_update_with_percentages(self, new_version: str, max_surge_percent: int = 25, max_unavailable_percent: int = 25):
        """
        Execute rolling update with percentage-based parameters
        
        Args:
            new_version: Version to deploy
            max_surge_percent: Maximum extra pods as percentage of replicas
            max_unavailable_percent: Maximum unavailable pods as percentage of replicas
        """
        print(f"\n🚀 STARTING ROLLING UPDATE (Percentage-based)")
        print(f"   Current: v{self.current_version}")
        print(f"   Target:  v{new_version}")
        print(f"   Strategy: maxSurge={max_surge_percent}%, maxUnavailable={max_unavailable_percent}%")
        print("=" * 60)
        
        # Calculate absolute values from percentages
        max_surge = max(1, int(self.replica_count * (max_surge_percent / 100)))
        max_unavailable = max(1, int(self.replica_count * (max_unavailable_percent / 100)))
        
        print(f"   Calculated: maxSurge={max_surge} pods, maxUnavailable={max_unavailable} pods")
        
        # Use the absolute value method
        self.rolling_update(new_version, max_surge, max_unavailable)
    
    def _get_running_pods_by_version(self, version: str = None) -> List[Pod]:
        """Get running pods, optionally filtered by version"""
        running = [p for p in self.pods if p.status == PodStatus.RUNNING]
        if version:
            return [p for p in running if p.version == version]
        return running
    
    def _get_running_pods(self) -> List[Pod]:
        """Get all running pods"""
        return [p for p in self.pods if p.status == PodStatus.RUNNING]
    
    def _create_new_pod(self, version: str):
        """Create and start a new pod"""
        # Find next available ID
        pod_num = len([p for p in self.pods if p.version == version])
        
        pod = Pod(
            id=f"{self.app_name}-v{version}-{pod_num:03d}",
            version=version,
            status=PodStatus.PENDING,
            is_ready=False
        )
        self.pods.append(pod)
        
        # Simulate pod startup
        print(f"     ⏳ Starting {pod.id}...")
        time.sleep(1.5)  # Simulate container pulling and startup
        
        # Simulate readiness check
        pod.status = PodStatus.RUNNING
        pod.is_ready = True
        print(f"     ✅ {pod.id} is ready")
    
    def _terminate_old_pod(self, pod: Pod):
        """Terminate an old pod"""
        print(f"     ⏳ Terminating {pod.id}...")
        pod.status = PodStatus.TERMINATED
        time.sleep(1)  # Simulate graceful shutdown
        print(f"     ✅ {pod.id} terminated")
    
    def display_state(self, title: str):
        """Display current deployment state"""
        print(f"\n📋 {title}")
        print("-" * 60)
        
        # Count pods by version and status
        stats = {}
        for pod in self.pods:
            key = (pod.version, pod.status)
            if key not in stats:
                stats[key] = 0
            stats[key] += 1
        
        # Display summary
        print("Deployment Status:")
        for (version, status), count in sorted(stats.items()):
            icon = "🟢" if status == PodStatus.RUNNING else "⚫" if status == PodStatus.TERMINATED else "🟡"
            print(f"  {icon} v{version}: {count} pods ({status.value})")
        
        # Display pod details
        print("\nPod Details:")
        running_pods = self._get_running_pods()
        for pod in sorted(running_pods, key=lambda p: p.id):
            print(f"  • {pod}")
        
        # Calculate availability
        total_running = len(running_pods)
        availability = (total_running / self.replica_count) * 100
        print(f"\n📈 Availability: {total_running}/{self.replica_count} pods ({availability:.1f}%)")
        
        if availability == 100:
            print("✅ Full availability maintained")
        elif availability >= 80:
            print("⚠️  Slightly reduced capacity")
        else:
            print("🔴 Significantly reduced capacity")
        
        print("-" * 60)

# ========== EXAMPLE SCENARIOS ==========
def demonstrate_different_strategies():
    """Demonstrate different rolling update configurations"""
    print("=" * 70)
    print("ROLLING DEPLOYMENT STRATEGY DEMONSTRATIONS")
    print("=" * 70)
    
    scenarios = [
        {
            "name": "Conservative Update (Safe)",
            "max_surge": 1,
            "max_unavailable": 0,
            "description": "Always maintain full capacity. Slow but safe."
        },
        {
            "name": "Balanced Update (Default)",
            "max_surge": 1,
            "max_unavailable": 1,
            "description": "Balance speed and safety. One pod can be down."
        },
        {
            "name": "Fast Update (Aggressive)",
            "max_surge": 2,
            "max_unavailable": 2,
            "description": "Update faster but with more risk."
        },
        {
            "name": "Percentage-based Update",
            "percentage": True,
            "max_surge_percent": 25,
            "max_unavailable_percent": 25,
            "description": "Using percentages instead of absolute numbers."
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n\n{'#' * 70}")
        print(f"SCENARIO {i}: {scenario['name']}")
        print(f"{'#' * 70}")
        print(f"Description: {scenario['description']}")
        
        # Create new deployment for each scenario
        deployment = RollingDeployment("webapp", "1.0")
        deployment.initialize_deployment(replica_count=6)
        
        print("\nPress Enter to start this scenario...")
        input()
        
        if scenario.get("percentage", False):
            deployment.rolling_update_with_percentages(
                new_version="2.0",
                max_surge_percent=scenario["max_surge_percent"],
                max_unavailable_percent=scenario["max_unavailable_percent"]
            )
        else:
            deployment.rolling_update(
                new_version="2.0",
                max_surge=scenario["max_surge"],
                max_unavailable=scenario["max_unavailable"]
            )
        
        print("\nPress Enter for next scenario...")
        input()

def simple_example():
    """Simple example of rolling deployment"""
    print("=" * 70)
    print("SIMPLE ROLLING DEPLOYMENT EXAMPLE")
    print("=" * 70)
    
    deployment = RollingDeployment("myapp", "1.0")
    deployment.initialize_deployment(replica_count=4)
    
    print("\nPress Enter to start rolling update...")
    input()
    
    deployment.rolling_update(
        new_version="2.0",
        max_surge=1,
        max_unavailable=1
    )

# ========== MAIN ==========
if __name__ == "__main__":
    # Uncomment which example you want to run
    
    # Simple example
    simple_example()
    
    # Multiple scenarios demonstration
    # demonstrate_different_strategies()