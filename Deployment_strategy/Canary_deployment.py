#!/usr/bin/env python3
"""
CANARY DEPLOYMENT STRATEGY

Purpose: Gradually roll out new version to a small subset of users (1:4 ratio = 20%)
         to test in production before full deployment.

Key Characteristics:
- Low risk deployment
- Real user testing
- Easy rollback if issues detected
- Progressive traffic shifting
"""

import time
import random
from typing import List, Dict, Any
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
    traffic_percentage: float = 0.0  # % of traffic this pod handles
    
    def __str__(self):
        return f"Pod-{self.id} (v{self.version}, {self.status.value}, {self.traffic_percentage}% traffic)"

@dataclass 
class DeploymentMetrics:
    error_rate: float
    latency_ms: float
    cpu_usage: float
    memory_usage: float

# ========== CANARY DEPLOYMENT CLASS ==========
class CanaryDeployment:
    """
    Simulates a Canary Deployment Strategy
    
    Typical flow:
    1. Deploy new version to small % of pods (e.g., 20% = 1:4 ratio)
    2. Route small % of traffic to new version
    3. Monitor metrics (errors, latency, etc.)
    4. If metrics look good, gradually increase traffic
    5. If issues detected, immediately rollback
    6. Eventually replace all old pods
    
    Common use cases:
    - Testing new features with real users
    - A/B testing
    - High-risk deployments
    """
    
    def __init__(self, app_name: str, initial_version: str = "1.0"):
        self.app_name = app_name
        self.current_version = initial_version
        self.new_version = None
        self.pods = []
        self.metrics_history = []
        self.total_traffic = 100  # Percentage
        
    def initialize_deployment(self, replica_count: int = 5):
        """Initialize with all pods running old version"""
        print(f"🔧 Initializing {self.app_name} deployment with {replica_count} pods")
        self.pods = []
        
        # Evenly distribute traffic among all pods
        traffic_per_pod = self.total_traffic / replica_count
        
        for i in range(replica_count):
            pod = Pod(
                id=f"{self.app_name}-{i:03d}",
                version=self.current_version,
                status=PodStatus.RUNNING,
                is_ready=True,
                traffic_percentage=traffic_per_pod
            )
            self.pods.append(pod)
        
        self.display_state("Initial Deployment")
    
    def deploy_canary(self, new_version: str, initial_percentage: float = 0.2):
        """
        Start canary deployment
        
        Args:
            new_version: The new version to deploy
            initial_percentage: Initial traffic percentage for canary (default 20% = 1:4 ratio)
        """
        print(f"\n🚀 STARTING CANARY DEPLOYMENT")
        print(f"   Old Version: v{self.current_version}")
        print(f"   New Version: v{new_version}")
        print(f"   Canary Size: {initial_percentage*100:.0f}% of traffic (1:{int(1/initial_percentage)} ratio)")
        print("=" * 60)
        
        self.new_version = new_version
        
        # Step 1: Deploy canary pods (but don't route traffic yet)
        print("\n📦 STEP 1: Deploying Canary Pods")
        canary_pods = self._deploy_canary_pods(initial_percentage)
        
        # Step 2: Start routing traffic to canary
        print("\n🔄 STEP 2: Routing Traffic to Canary")
        self._route_traffic_to_canary(canary_pods, initial_percentage)
        
        # Step 3: Monitor canary
        print(f"\n📊 STEP 3: Monitoring Canary (30 seconds)")
        monitoring_success = self._monitor_canary(canary_pods, duration=30)
        
        if monitoring_success:
            # Step 4: Gradual rollout
            print("\n📈 STEP 4: Gradual Rollout")
            self._gradual_rollout(canary_pods)
            
            # Step 5: Complete rollout
            print("\n✅ STEP 5: Completing Rollout")
            self._complete_rollout()
        else:
            # Rollback if monitoring fails
            print("\n❌ STEP 4: Rolling Back (Issues Detected)")
            self._rollback_canary(canary_pods)
    
    def _deploy_canary_pods(self, percentage: float) -> List[Pod]:
        """Deploy initial canary pods"""
        # Calculate how many canary pods to deploy (minimum 1)
        total_pods = len([p for p in self.pods if p.status == PodStatus.RUNNING])
        canary_count = max(1, int(total_pods * percentage))
        
        canary_pods = []
        for i in range(canary_count):
            pod = Pod(
                id=f"{self.app_name}-canary-{i:03d}",
                version=self.new_version,
                status=PodStatus.PENDING,
                is_ready=False,
                traffic_percentage=0.0  # No traffic yet
            )
            self.pods.append(pod)
            canary_pods.append(pod)
            
            # Simulate pod startup
            print(f"   ⏳ Starting {pod.id}...")
            time.sleep(0.5)
            pod.status = PodStatus.RUNNING
            pod.is_ready = True
            print(f"   ✅ {pod.id} is ready")
        
        print(f"   Deployed {len(canary_pods)} canary pods (v{self.new_version})")
        return canary_pods
    
    def _route_traffic_to_canary(self, canary_pods: List[Pod], percentage: float):
        """Route specified percentage of traffic to canary pods"""
        print(f"   Routing {percentage*100:.0f}% of traffic to canary pods")
        
        # Reduce traffic from old pods
        old_pods = [p for p in self.pods 
                   if p.status == PodStatus.RUNNING and p.version == self.current_version]
        
        # Calculate traffic distribution
        traffic_to_old = (1 - percentage) * self.total_traffic
        traffic_to_canary = percentage * self.total_traffic
        
        # Update traffic percentages
        for pod in old_pods:
            pod.traffic_percentage = traffic_to_old / len(old_pods)
        
        for pod in canary_pods:
            pod.traffic_percentage = traffic_to_canary / len(canary_pods)
        
        self.display_state(f"Traffic Routing: {percentage*100:.0f}% to Canary")
    
    def _monitor_canary(self, canary_pods: List[Pod], duration: int = 30) -> bool:
        """Monitor canary metrics and decide if rollout should continue"""
        print("   Monitoring metrics...")
        print("   [Key metrics: Error Rate (< 1%), Latency (< 200ms), CPU (< 80%), Memory (< 90%)]")
        print("   " + "-" * 50)
        
        checks_passed = 0
        total_checks = duration // 5  # Check every 5 seconds
        
        for check in range(total_checks):
            time.sleep(5)  # Wait between checks
            
            # Simulate collecting metrics
            metrics = self._collect_metrics(canary_pods)
            self.metrics_history.append(metrics)
            
            # Display current metrics
            print(f"   Check {check+1}/{total_checks}: ", end="")
            print(f"Errors: {metrics.error_rate:.1f}% | ", end="")
            print(f"Latency: {metrics.latency_ms:.0f}ms | ", end="")
            print(f"CPU: {metrics.cpu_usage:.0f}% | ", end="")
            print(f"Memory: {metrics.memory_usage:.0f}%")
            
            # Evaluate metrics
            if self._evaluate_metrics(metrics):
                checks_passed += 1
                print(f"   ✅ Metrics OK ({checks_passed}/{total_checks} checks passed)")
            else:
                print(f"   ⚠️  Metrics concerning ({checks_passed}/{total_checks} checks passed)")
        
        # Decide based on metrics
        success_rate = checks_passed / total_checks
        print(f"\n   📈 Canary Success Rate: {success_rate*100:.1f}%")
        
        if success_rate >= 0.8:  # 80% of checks passed
            print("   ✅ Canary successful! Proceeding with rollout.")
            return True
        else:
            print("   ❌ Canary failed! Too many metric violations.")
            return False
    
    def _collect_metrics(self, canary_pods: List[Pod]) -> DeploymentMetrics:
        """Simulate collecting deployment metrics"""
        # In real scenario, this would collect from monitoring system
        # Here we simulate with some randomness and slight bias toward success
        
        base_error = random.uniform(0.1, 1.5)  # 0.1% to 1.5%
        base_latency = random.uniform(80, 180)  # 80-180ms
        base_cpu = random.uniform(40, 75)  # 40-75%
        base_memory = random.uniform(50, 85)  # 50-85%
        
        return DeploymentMetrics(
            error_rate=base_error,
            latency_ms=base_latency,
            cpu_usage=base_cpu,
            memory_usage=base_memory
        )
    
    def _evaluate_metrics(self, metrics: DeploymentMetrics) -> bool:
        """Evaluate if metrics are within acceptable ranges"""
        return (
            metrics.error_rate < 1.0 and      # Less than 1% errors
            metrics.latency_ms < 200 and      # Less than 200ms latency
            metrics.cpu_usage < 80 and        # Less than 80% CPU
            metrics.memory_usage < 90         # Less than 90% memory
        )
    
    def _gradual_rollout(self, initial_canary_pods: List[Pod]):
        """Gradually increase traffic to new version"""
        print("   Gradually increasing traffic to new version...")
        
        # Traffic increase steps: 20% → 50% → 80% → 100%
        traffic_steps = [0.5, 0.8, 1.0]
        
        for step_num, target_percentage in enumerate(traffic_steps, 1):
            print(f"\n   Step {step_num}: Increasing to {target_percentage*100:.0f}% traffic")
            
            # Deploy more pods if needed
            current_new_pods = [p for p in self.pods 
                              if p.status == PodStatus.RUNNING and p.version == self.new_version]
            current_old_pods = [p for p in self.pods 
                              if p.status == PodStatus.RUNNING and p.version == self.current_version]
            
            # Calculate needed pods for target percentage
            total_needed_pods = len(current_new_pods) + len(current_old_pods)
            needed_new_pods = int(total_needed_pods * target_percentage)
            
            # Deploy additional pods if needed
            if len(current_new_pods) < needed_new_pods:
                pods_to_add = needed_new_pods - len(current_new_pods)
                print(f"   Deploying {pods_to_add} additional v{self.new_version} pods")
                for i in range(pods_to_add):
                    self._deploy_additional_pod()
            
            # Route traffic
            self._route_traffic_to_new_version(target_percentage)
            
            # Monitor for a bit
            print(f"   Monitoring at {target_percentage*100:.0f}% traffic...")
            time.sleep(10)
            
            # Quick metric check
            metrics = self._collect_metrics([])
            if self._evaluate_metrics(metrics):
                print(f"   ✅ Step {step_num} successful")
            else:
                print(f"   ⚠️  Minor issues at {target_percentage*100:.0f}%, but continuing")
    
    def _deploy_additional_pod(self):
        """Deploy one additional new version pod"""
        pod_id = len([p for p in self.pods if p.version == self.new_version])
        pod = Pod(
            id=f"{self.app_name}-new-{pod_id:03d}",
            version=self.new_version,
            status=PodStatus.PENDING,
            is_ready=False,
            traffic_percentage=0.0
        )
        self.pods.append(pod)
        
        time.sleep(0.5)  # Simulate startup
        pod.status = PodStatus.RUNNING
        pod.is_ready = True
    
    def _route_traffic_to_new_version(self, percentage: float):
        """Route traffic between old and new versions"""
        new_pods = [p for p in self.pods 
                   if p.status == PodStatus.RUNNING and p.version == self.new_version]
        old_pods = [p for p in self.pods 
                   if p.status == PodStatus.RUNNING and p.version == self.current_version]
        
        # Update traffic distribution
        traffic_to_new = percentage * self.total_traffic
        traffic_to_old = (1 - percentage) * self.total_traffic
        
        if new_pods:
            for pod in new_pods:
                pod.traffic_percentage = traffic_to_new / len(new_pods)
        
        if old_pods:
            for pod in old_pods:
                pod.traffic_percentage = traffic_to_old / len(old_pods)
    
    def _complete_rollout(self):
        """Complete the rollout by replacing all old pods"""
        print("   Completing rollout...")
        
        # Terminate all remaining old pods
        old_pods = [p for p in self.pods 
                   if p.status == PodStatus.RUNNING and p.version == self.current_version]
        
        for pod in old_pods:
            print(f"   Terminating {pod.id}")
            pod.status = PodStatus.TERMINATED
            pod.traffic_percentage = 0.0
            time.sleep(0.3)
        
        # Update current version
        self.current_version = self.new_version
        
        # Rebalance traffic among remaining pods
        new_pods = [p for p in self.pods if p.status == PodStatus.RUNNING]
        traffic_per_pod = self.total_traffic / len(new_pods) if new_pods else 0
        
        for pod in new_pods:
            pod.traffic_percentage = traffic_per_pod
        
        print(f"\n   ✅ Rollout complete! All traffic now on v{self.current_version}")
        self.display_state("Final State")
    
    def _rollback_canary(self, canary_pods: List[Pod]):
        """Rollback canary deployment"""
        print("   Initiating rollback...")
        
        # Terminate all canary pods
        for pod in canary_pods:
            print(f"   Terminating canary pod {pod.id}")
            pod.status = PodStatus.TERMINATED
            pod.traffic_percentage = 0.0
            time.sleep(0.3)
        
        # Route all traffic back to old version
        old_pods = [p for p in self.pods 
                   if p.status == PodStatus.RUNNING and p.version == self.current_version]
        
        traffic_per_pod = self.total_traffic / len(old_pods) if old_pods else 0
        for pod in old_pods:
            pod.traffic_percentage = traffic_per_pod
        
        print(f"\n   ✅ Rollback complete! All traffic back on v{self.current_version}")
        self.display_state("Rollback Complete")
    
    def display_state(self, title: str):
        """Display current deployment state"""
        print(f"\n📋 {title}")
        print("-" * 60)
        
        # Group pods by version
        pods_by_version = {}
        for pod in self.pods:
            if pod.version not in pods_by_version:
                pods_by_version[pod.version] = []
            pods_by_version[pod.version].append(pod)
        
        # Display each version
        for version in sorted(pods_by_version.keys()):
            pods = pods_by_version[version]
            running = [p for p in pods if p.status == PodStatus.RUNNING]
            traffic_percentage = sum(p.traffic_percentage for p in running)
            
            print(f"\nVersion {version}:")
            print(f"  Running: {len(running)} pods")
            print(f"  Traffic: {traffic_percentage:.1f}%")
            
            if running:
                print("  Pods:", end=" ")
                pod_names = [p.id.split('-')[-1] for p in running[:3]]
                print(", ".join(pod_names), end="")
                if len(running) > 3:
                    print(f" ... and {len(running)-3} more")
                else:
                    print()
        
        print("-" * 60)

# ========== EXAMPLE USAGE ==========
def main():
    """Example of canary deployment"""
    print("=" * 70)
    print("CANARY DEPLOYMENT STRATEGY DEMONSTRATION")
    print("=" * 70)
    print("\n📖 Scenario: Deploying new version with 1:4 ratio (20% traffic initially)")
    print("   This allows testing with real users before full rollout")
    print("\nPress Enter to start...")
    input()
    
    # Create deployment
    deployment = CanaryDeployment("webapp", "1.0")
    
    # Initialize with 5 pods
    deployment.initialize_deployment(replica_count=5)
    
    # Start canary deployment
    deployment.deploy_canary(
        new_version="2.0",
        initial_percentage=0.2  # 20% = 1:4 ratio
    )

if __name__ == "__main__":
    main()