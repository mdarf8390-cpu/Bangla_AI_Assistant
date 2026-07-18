import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class RequestStatus(Enum):
    """Status of feature request"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    ON_HOLD = "on_hold"


class Priority(Enum):
    """Priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FeatureRequest:
    """Individual feature request"""
    
    def __init__(self, request_id: str, description: str, requested_by: str):
        self.id = request_id
        self.description = description
        self.requested_by = requested_by
        self.created_at = datetime.now()
        self.status = RequestStatus.PENDING
        self.priority = Priority.MEDIUM
        self.implementation_notes = ""
        self.estimated_time = None
        self.completed_at = None
        self.error_handling = "Not specified"
        self.dependencies = []
        self.tags = []
        
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "requested_by": self.requested_by,
            "created_at": self.created_at.isoformat(),
            "status": self.status.value,
            "priority": self.priority.value,
            "implementation_notes": self.implementation_notes,
            "estimated_time": self.estimated_time,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_handling": self.error_handling,
            "dependencies": self.dependencies,
            "tags": self.tags
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'FeatureRequest':
        """Create from dictionary"""
        req = FeatureRequest(data["id"], data["description"], data["requested_by"])
        req.created_at = datetime.fromisoformat(data["created_at"])
        req.status = RequestStatus(data["status"])
        req.priority = Priority(data["priority"])
        req.implementation_notes = data.get("implementation_notes", "")
        req.estimated_time = data.get("estimated_time")
        req.error_handling = data.get("error_handling", "Not specified")
        req.dependencies = data.get("dependencies", [])
        req.tags = data.get("tags", [])
        if data.get("completed_at"):
            req.completed_at = datetime.fromisoformat(data["completed_at"])
        return req


class FeatureRequestSystem:
    """System to manage feature requests"""
    
    def __init__(self, storage_path: str = "feature_requests.json"):
        self.storage_path = storage_path
        self.requests: Dict[str, FeatureRequest] = {}
        self.request_counter = 0
        self.load_requests()
    
    def load_requests(self):
        """Load requests from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for req_id, req_data in data.get("requests", {}).items():
                        self.requests[req_id] = FeatureRequest.from_dict(req_data)
                    self.request_counter = data.get("counter", len(self.requests))
                logger.info(f"Loaded {len(self.requests)} feature requests")
            else:
                logger.info("No existing requests found")
        except Exception as e:
            logger.error(f"Error loading requests: {str(e)}")
    
    def save_requests(self):
        """Save requests to storage"""
        try:
            data = {
                "requests": {
                    req_id: req.to_dict()
                    for req_id, req in self.requests.items()
                },
                "counter": self.request_counter
            }
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("Requests saved successfully")
        except Exception as e:
            logger.error(f"Error saving requests: {str(e)}")
    
    def add_feature_request(self, description: str, requested_by: str, 
                           priority: str = "medium", error_handling: str = None) -> tuple:
        """Add a new feature request"""
        try:
            self.request_counter += 1
            request_id = f"FR{self.request_counter:04d}"
            
            request = FeatureRequest(request_id, description, requested_by)
            
            # Set priority
            try:
                request.priority = Priority[priority.upper()]
            except (KeyError, AttributeError):
                request.priority = Priority.MEDIUM
            
            # Set error handling info
            if error_handling:
                request.error_handling = error_handling
            
            self.requests[request_id] = request
            self.save_requests()
            
            response = f"""✅ Feature request created successfully!
📋 Request ID: {request_id}
📝 Description: {description}
👤 Requested by: {requested_by}
⚡ Priority: {request.priority.value.upper()}
🛡️ Error Handling: {request.error_handling}

আমি এই feature implement করার চেষ্টা করব। ধন্যবাদ suggestion এর জন্য!"""
            
            return True, response, request_id
        
        except Exception as e:
            logger.error(f"Error adding request: {str(e)}")
            return False, f"❌ Error: {str(e)}", None
    
    def get_request_status(self, request_id: str) -> str:
        """Get status of a specific request"""
        try:
            if request_id not in self.requests:
                return f"❌ Request {request_id} found না।"
            
            req = self.requests[request_id]
            status_emoji = {
                RequestStatus.PENDING: "⏳",
                RequestStatus.IN_PROGRESS: "🚀",
                RequestStatus.COMPLETED: "✅",
                RequestStatus.REJECTED: "❌",
                RequestStatus.ON_HOLD: "⏸️"
            }
            
            response = f"""📋 Feature Request Details:
ID: {req.id}
📝 Description: {req.description}
👤 Requested by: {req.requested_by}
📅 Created: {req.created_at.strftime('%Y-%m-%d %H:%M')}
{status_emoji.get(req.status, "❓")} Status: {req.status.value.upper()}
⚡ Priority: {req.priority.value.upper()}
🛡️ Error Handling: {req.error_handling}"""
            
            if req.implementation_notes:
                response += f"\n📝 Notes: {req.implementation_notes}"
            
            if req.completed_at:
                response += f"\n✅ Completed: {req.completed_at.strftime('%Y-%m-%d %H:%M')}"
            
            return response
        
        except Exception as e:
            logger.error(f"Error getting request status: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def list_all_requests(self, status: str = None) -> str:
        """List all or filtered requests"""
        try:
            if not self.requests:
                return "📭 কোন feature request নেই।"
            
            filtered_requests = self.requests.values()
            
            if status:
                try:
                    status_enum = RequestStatus[status.upper()]
                    filtered_requests = [r for r in filtered_requests if r.status == status_enum]
                except KeyError:
                    pass
            
            if not filtered_requests:
                return f"📭 No requests found with status '{status}'।"
            
            response = "📋 All Feature Requests:\n\n"
            for req in sorted(filtered_requests, key=lambda x: x.priority.value, reverse=True):
                status_emoji = {
                    RequestStatus.PENDING: "⏳",
                    RequestStatus.IN_PROGRESS: "🚀",
                    RequestStatus.COMPLETED: "✅",
                    RequestStatus.REJECTED: "❌",
                    RequestStatus.ON_HOLD: "⏸️"
                }
                
                priority_emoji = {
                    Priority.CRITICAL: "🔴",
                    Priority.HIGH: "🟠",
                    Priority.MEDIUM: "🟡",
                    Priority.LOW: "🟢"
                }
                
                response += f"{req.id} | {status_emoji.get(req.status, '❓')} {req.status.value.upper()} | {priority_emoji.get(req.priority, '❓')} {req.priority.value.upper()}\n"
                response += f"   📝 {req.description}\n"
                response += f"   👤 By: {req.requested_by}\n\n"
            
            return response
        
        except Exception as e:
            logger.error(f"Error listing requests: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def update_request_status(self, request_id: str, new_status: str) -> str:
        """Update request status"""
        try:
            if request_id not in self.requests:
                return f"❌ Request {request_id} found না।"
            
            req = self.requests[request_id]
            try:
                req.status = RequestStatus[new_status.upper()]
                if new_status.upper() == "COMPLETED":
                    req.completed_at = datetime.now()
                self.save_requests()
                return f"✅ {request_id} status updated to {req.status.value}!"
            except KeyError:
                return f"❌ Invalid status: {new_status}"
        
        except Exception as e:
            logger.error(f"Error updating status: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def add_implementation_notes(self, request_id: str, notes: str) -> str:
        """Add implementation notes to a request"""
        try:
            if request_id not in self.requests:
                return f"❌ Request {request_id} found না।"
            
            req = self.requests[request_id]
            req.implementation_notes = notes
            self.save_requests()
            return f"✅ Notes added to {request_id}!"
        
        except Exception as e:
            logger.error(f"Error adding notes: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def set_priority(self, request_id: str, priority: str) -> str:
        """Set priority of a request"""
        try:
            if request_id not in self.requests:
                return f"❌ Request {request_id} found না।"
            
            req = self.requests[request_id]
            try:
                req.priority = Priority[priority.upper()]
                self.save_requests()
                return f"✅ Priority of {request_id} set to {req.priority.value}!"
            except KeyError:
                return f"❌ Invalid priority: {priority}"
        
        except Exception as e:
            logger.error(f"Error setting priority: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def get_high_priority_requests(self) -> str:
        """Get all high and critical priority requests"""
        try:
            high_priority = [r for r in self.requests.values() 
                           if r.priority in [Priority.HIGH, Priority.CRITICAL]]
            
            if not high_priority:
                return "🟢 কোন urgent request নেই।"
            
            response = "🚨 High Priority Requests:\n\n"
            for req in sorted(high_priority, key=lambda x: x.priority.value, reverse=True):
                response += f"🔴 {req.id} | {req.description}\n"
                response += f"   👤 By: {req.requested_by}\n"
                response += f"   Status: {req.status.value}\n\n"
            
            return response
        
        except Exception as e:
            logger.error(f"Error getting high priority: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def get_statistics(self) -> str:
        """Get statistics about all requests"""
        try:
            total = len(self.requests)
            pending = len([r for r in self.requests.values() if r.status == RequestStatus.PENDING])
            in_progress = len([r for r in self.requests.values() if r.status == RequestStatus.IN_PROGRESS])
            completed = len([r for r in self.requests.values() if r.status == RequestStatus.COMPLETED])
            rejected = len([r for r in self.requests.values() if r.status == RequestStatus.REJECTED])
            
            response = f"""📊 Feature Request Statistics:
📝 Total Requests: {total}
⏳ Pending: {pending}
🚀 In Progress: {in_progress}
✅ Completed: {completed}
❌ Rejected: {rejected}

Completion Rate: {(completed/total*100):.1f}% if total > 0 else 0%
Progress: {'█' * completed}{'░' * (total-completed)}"""
            
            return response
        
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return f"❌ Error: {str(e)}"


# Global instance
feature_request_system = None


def initialize_feature_system(storage_path: str = "feature_requests.json") -> FeatureRequestSystem:
    """Initialize global feature request system"""
    global feature_request_system
    feature_request_system = FeatureRequestSystem(storage_path)
    return feature_request_system


def get_feature_system() -> FeatureRequestSystem:
    """Get global feature request system"""
    global feature_request_system
    if feature_request_system is None:
        feature_request_system = FeatureRequestSystem()
    return feature_request_system
