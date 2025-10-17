from nicegui import ui, app
from helperFuns import imagePath
from assets import FlipCards, SearchBox
import asyncio
from datetime import datetime, timedelta, date
import json
import uuid
import hashlib

# Smart Employee Probation Management System with Advanced HR Algorithms
class ProbationManager:
    """
    Intelligent probation management system with smart algorithms for
    probation tracking, performance monitoring, and automated assessments
    """
    
    def __init__(self):
        # Probation types and configurations
        self.probation_types = {
            "Initial Probation": {
                "code": "IP",
                "duration_months": 6,
                "review_intervals": [1, 3, 6],  # months
                "auto_extension_allowed": True,
                "max_extensions": 1,
                "performance_threshold": 70,
                "color": "blue"
            },
            "Extended Probation": {
                "code": "EP", 
                "duration_months": 3,
                "review_intervals": [1, 2, 3],
                "auto_extension_allowed": False,
                "max_extensions": 0,
                "performance_threshold": 75,
                "color": "orange"
            },
            "Performance Improvement": {
                "code": "PIP",
                "duration_months": 3,
                "review_intervals": [1, 2, 3],
                "auto_extension_allowed": True,
                "max_extensions": 2,
                "performance_threshold": 80,
                "color": "red"
            },
            "Disciplinary Probation": {
                "code": "DP",
                "duration_months": 6,
                "review_intervals": [1, 3, 6],
                "auto_extension_allowed": False,
                "max_extensions": 0,
                "performance_threshold": 85,
                "color": "purple"
            },
            "Post-Transfer Probation": {
                "code": "PTP",
                "duration_months": 3,
                "review_intervals": [1, 3],
                "auto_extension_allowed": True,
                "max_extensions": 1,
                "performance_threshold": 75,
                "color": "green"
            }
        }
        
        # Mock employee data for probation
        self.employees = [
            {
                "id": "EMP-101",
                "name": "Alice Johnson",
                "department": "Marketing",
                "position": "Marketing Specialist",
                "start_date": "2024-08-01",
                "manager_id": "MGR-001",
                "manager_name": "David Thompson",
                "security_clearance": "Standard",
                "is_new_hire": True
            },
            {
                "id": "EMP-102", 
                "name": "Robert Chen",
                "department": "Information Technology",
                "position": "Junior Developer",
                "start_date": "2024-07-15",
                "manager_id": "MGR-002",
                "manager_name": "Michael Chen",
                "security_clearance": "Standard",
                "is_new_hire": True
            },
            {
                "id": "EMP-103",
                "name": "Maria Garcia",
                "department": "Human Resources",
                "position": "HR Assistant",
                "start_date": "2024-06-01",
                "manager_id": "MGR-003",
                "manager_name": "Sarah Johnson",
                "security_clearance": "Standard",
                "is_new_hire": False
            }
        ]
        
        # Existing probation records
        self.probation_records = [
            {
                "id": "PROB-001",
                "employee_id": "EMP-101",
                "employee_name": "Alice Johnson",
                "probation_type": "Initial Probation",
                "start_date": "2024-08-01",
                "end_date": "2025-02-01",
                "status": "Active",
                "current_score": 78,
                "completion_percentage": 45,
                "next_review_date": "2024-11-01",
                "goals_set": 5,
                "goals_achieved": 3,
                "manager_id": "MGR-001",
                "created_by": "HR-001",
                "created_date": "2024-08-01",
                "smart_recommendations": ["Focus on technical skills", "Improve communication"],
                "risk_level": "Low"
            },
            {
                "id": "PROB-002",
                "employee_id": "EMP-102",
                "employee_name": "Robert Chen",
                "probation_type": "Initial Probation", 
                "start_date": "2024-07-15",
                "end_date": "2025-01-15",
                "status": "Active",
                "current_score": 65,
                "completion_percentage": 60,
                "next_review_date": "2024-10-15",
                "goals_set": 6,
                "goals_achieved": 2,
                "manager_id": "MGR-002",
                "created_by": "HR-001", 
                "created_date": "2024-07-15",
                "smart_recommendations": ["Require additional training", "Weekly check-ins needed"],
                "risk_level": "Medium"
            },
            {
                "id": "PROB-003",
                "employee_id": "EMP-103",
                "employee_name": "Maria Garcia",
                "probation_type": "Performance Improvement",
                "start_date": "2024-09-01",
                "end_date": "2024-12-01",
                "status": "Under Review",
                "current_score": 72,
                "completion_percentage": 33,
                "next_review_date": "2024-10-01",
                "goals_set": 4,
                "goals_achieved": 2,
                "manager_id": "MGR-003",
                "created_by": "HR-001",
                "created_date": "2024-09-01", 
                "smart_recommendations": ["Performance coaching required", "Set clearer expectations"],
                "risk_level": "High"
            }
        ]
        
        # Performance tracking metrics
        self.performance_metrics = {
            "Job Knowledge": {"weight": 25, "description": "Understanding of role and responsibilities"},
            "Quality of Work": {"weight": 20, "description": "Accuracy and thoroughness of work output"},
            "Productivity": {"weight": 20, "description": "Efficiency and quantity of work completed"},
            "Communication": {"weight": 15, "description": "Verbal and written communication skills"},
            "Teamwork": {"weight": 10, "description": "Collaboration and interpersonal skills"},
            "Initiative": {"weight": 10, "description": "Proactiveness and problem-solving ability"}
        }
        
        # Smart algorithm configurations
        self.algorithm_settings = {
            "risk_assessment_factors": {
                "performance_below_threshold": 30,
                "missed_review_deadlines": 20,
                "goal_achievement_ratio": 25,
                "manager_feedback_negative": 15,
                "attendance_issues": 10
            },
            "auto_recommendation_triggers": {
                "low_performance": 60,
                "missed_goals": 50,
                "poor_communication": 40
            },
            "success_prediction_model": {
                "current_score_weight": 40,
                "improvement_trend_weight": 30,
                "goal_achievement_weight": 20,
                "manager_rating_weight": 10
            }
        }

    def calculate_probation_score(self, probation_data, performance_reviews=None):
        """Advanced algorithm to calculate overall probation performance score"""
        base_score = 60  # Starting point
        
        # Performance review scores (if available)
        if performance_reviews:
            review_scores = [review.get('overall_score', 0) for review in performance_reviews]
            if review_scores:
                avg_review_score = sum(review_scores) / len(review_scores)
                base_score = avg_review_score
        
        # Goal achievement factor
        goals_set = probation_data.get('goals_set', 0)
        goals_achieved = probation_data.get('goals_achieved', 0)
        
        if goals_set > 0:
            goal_ratio = goals_achieved / goals_set
            goal_score = goal_ratio * 20  # Up to 20 points
            base_score += goal_score
        
        # Time progression factor
        start_date = datetime.strptime(probation_data.get('start_date', ''), '%Y-%m-%d').date()
        end_date = datetime.strptime(probation_data.get('end_date', ''), '%Y-%m-%d').date()
        total_duration = (end_date - start_date).days
        elapsed_days = (date.today() - start_date).days
        
        if total_duration > 0:
            progress_ratio = min(elapsed_days / total_duration, 1.0)
            # Expect steady improvement over time
            expected_improvement = progress_ratio * 15  # Up to 15 points
            base_score += expected_improvement
        
        # Manager feedback integration (mock data)
        manager_satisfaction = probation_data.get('manager_satisfaction', 75)
        manager_weight = (manager_satisfaction - 50) * 0.2  # -10 to +10 points
        base_score += manager_weight
        
        return min(max(base_score, 0), 100)  # Clamp between 0-100

    def assess_risk_level(self, probation_record):
        """Smart risk assessment algorithm"""
        risk_score = 0
        
        current_score = probation_record.get('current_score', 0)
        probation_type = probation_record.get('probation_type', '')
        
        # Performance threshold check
        threshold = self.probation_types.get(probation_type, {}).get('performance_threshold', 70)
        if current_score < threshold:
            risk_score += self.algorithm_settings['risk_assessment_factors']['performance_below_threshold']
        
        # Goal achievement ratio
        goals_set = probation_record.get('goals_set', 1)
        goals_achieved = probation_record.get('goals_achieved', 0)
        goal_ratio = goals_achieved / goals_set if goals_set > 0 else 0
        
        if goal_ratio < 0.5:
            risk_score += self.algorithm_settings['risk_assessment_factors']['goal_achievement_ratio']
        
        # Review timeline compliance
        next_review = datetime.strptime(probation_record.get('next_review_date', ''), '%Y-%m-%d').date()
        if next_review < date.today():
            risk_score += self.algorithm_settings['risk_assessment_factors']['missed_review_deadlines']
        
        # Determine risk level
        if risk_score >= 60:
            return "High"
        elif risk_score >= 30:
            return "Medium"
        else:
            return "Low"

    def generate_smart_recommendations(self, probation_record):
        """AI-powered recommendation engine"""
        recommendations = []
        
        current_score = probation_record.get('current_score', 0)
        probation_type = probation_record.get('probation_type', '')
        goals_achieved = probation_record.get('goals_achieved', 0)
        goals_set = probation_record.get('goals_set', 1)
        
        # Performance-based recommendations
        if current_score < 65:
            recommendations.append({
                "type": "Performance Improvement",
                "priority": "High",
                "action": "Implement weekly performance coaching sessions",
                "timeline": "Immediate"
            })
        elif current_score < 75:
            recommendations.append({
                "type": "Skill Development", 
                "priority": "Medium",
                "action": "Enroll in relevant training programs",
                "timeline": "Within 2 weeks"
            })
        
        # Goal achievement recommendations
        goal_ratio = goals_achieved / goals_set if goals_set > 0 else 0
        if goal_ratio < 0.4:
            recommendations.append({
                "type": "Goal Setting",
                "priority": "High", 
                "action": "Revise and clarify performance goals with SMART criteria",
                "timeline": "Within 1 week"
            })
        
        # Probation type specific recommendations
        if probation_type == "Performance Improvement":
            recommendations.append({
                "type": "Intensive Support",
                "priority": "High",
                "action": "Assign dedicated mentor for daily guidance",
                "timeline": "Immediate"
            })
        elif probation_type == "Initial Probation" and current_score > 85:
            recommendations.append({
                "type": "Early Completion",
                "priority": "Medium",
                "action": "Consider early probation completion",
                "timeline": "Next review"
            })
        
        return recommendations

    def predict_probation_success(self, probation_record):
        """Machine learning-inspired success prediction"""
        weights = self.algorithm_settings['success_prediction_model']
        
        # Current performance score factor
        current_score = probation_record.get('current_score', 0)
        score_factor = (current_score / 100) * weights['current_score_weight']
        
        # Improvement trend factor (mock calculation)
        improvement_trend = 0.7  # Would be calculated from historical data
        trend_factor = improvement_trend * weights['improvement_trend_weight']
        
        # Goal achievement factor
        goals_set = probation_record.get('goals_set', 1)
        goals_achieved = probation_record.get('goals_achieved', 0)
        goal_ratio = goals_achieved / goals_set if goals_set > 0 else 0
        goal_factor = goal_ratio * weights['goal_achievement_weight']
        
        # Manager rating factor (mock)
        manager_rating = 0.8  # Would come from manager feedback
        manager_factor = manager_rating * weights['manager_rating_weight']
        
        success_probability = score_factor + trend_factor + goal_factor + manager_factor
        
        return min(max(success_probability, 0), 100)

    def get_probation_analytics(self):
        """Generate analytics for dashboard"""
        active_probations = [r for r in self.probation_records if r['status'] == 'Active']
        
        analytics = {
            "total_active": len(active_probations),
            "risk_distribution": {
                "High": len([r for r in active_probations if r.get('risk_level') == 'High']),
                "Medium": len([r for r in active_probations if r.get('risk_level') == 'Medium']),
                "Low": len([r for r in active_probations if r.get('risk_level') == 'Low'])
            },
            "average_score": sum(r.get('current_score', 0) for r in active_probations) / len(active_probations) if active_probations else 0,
            "completion_rate": sum(r.get('completion_percentage', 0) for r in active_probations) / len(active_probations) if active_probations else 0,
            "overdue_reviews": len([r for r in active_probations if datetime.strptime(r.get('next_review_date', ''), '%Y-%m-%d').date() < date.today()])
        }
        
        return analytics

    def create_probation_record(self, probation_data):
        """Create new probation record with smart initialization"""
        new_id = f"PROB-{str(uuid.uuid4())[:6].upper()}"
        
        probation_type = probation_data.get('probation_type')
        probation_config = self.probation_types.get(probation_type, {})
        
        # Calculate end date based on type
        start_date = datetime.strptime(probation_data.get('start_date'), '%Y-%m-%d').date()
        duration_months = probation_config.get('duration_months', 6)
        end_date = start_date + timedelta(days=duration_months * 30)  # Approximate
        
        # Set first review date
        review_intervals = probation_config.get('review_intervals', [1])
        first_review = start_date + timedelta(days=review_intervals[0] * 30)
        
        new_record = {
            "id": new_id,
            "end_date": end_date.strftime('%Y-%m-%d'),
            "status": "Active",
            "current_score": 60,  # Starting score
            "completion_percentage": 0,
            "next_review_date": first_review.strftime('%Y-%m-%d'),
            "goals_set": 0,
            "goals_achieved": 0,
            "created_by": "CURRENT_USER",
            "created_date": date.today().strftime('%Y-%m-%d'),
            "smart_recommendations": [],
            "risk_level": "Low",
            **probation_data
        }
        
        self.probation_records.append(new_record)
        return True, new_id

    def update_probation_record(self, record_id, updates):
        """Update probation record with automatic recalculation"""
        for record in self.probation_records:
            if record['id'] == record_id:
                record.update(updates)
                
                # Recalculate smart metrics
                record['current_score'] = self.calculate_probation_score(record)
                record['risk_level'] = self.assess_risk_level(record)
                record['smart_recommendations'] = self.generate_smart_recommendations(record)
                
                return True
        return False

# Global probation manager instance
probation_manager = ProbationManager()

def EmployeeProbation():
    """
    Modern Employee Probation Management page with AI-powered analytics
    """
    
    # Modern header with gradient background
    with ui.element('div').classes('w-full bg-gradient-to-r from-purple-600 via-purple-700 to-indigo-800 text-white p-8 rounded-xl shadow-2xl mb-8'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.column():
                ui.html('''
                    <div class="flex items-center gap-4">
                        <div class="bg-white bg-opacity-20 p-3 rounded-full">
                            <i class="material-icons text-4xl">psychology</i>
                        </div>
                        <div>
                            <h1 class="text-4xl font-bold mb-2">Employee Probation Management</h1>
                            <p class="text-purple-100 text-lg">AI-powered performance tracking and success prediction</p>
                        </div>
                    </div>
                ''', sanitize=False)
                
                # Breadcrumb navigation
                with ui.row().classes('items-center gap-2 text-sm text-purple-200 mt-4'):
                    ui.icon('home').classes('text-purple-300')
                    ui.label('Dashboard')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Administration')
                    ui.icon('chevron_right').classes('text-xs')
                    ui.label('Probation').classes('text-white font-medium')
            
            # Quick action buttons
            with ui.column().classes('gap-3'):
                ui.button('🧠 AI Analytics', on_click=show_ai_analytics_dialog).props('color=white text-color=purple-700').classes('font-semibold')
                ui.button('➕ New Probation', on_click=show_new_probation_dialog).props('outlined color=white').classes('font-semibold')

    # Smart statistics dashboard
    create_smart_dashboard()

    # Main content with modern tabs
    with ui.element('div').classes('w-full'):
        with ui.tabs().classes('w-full mb-6 bg-white rounded-lg shadow-lg') as tabs:
            tabs.props('indicator-color=purple-600 active-color=purple-600')
            overview_tab = ui.tab('📊 Overview', icon='dashboard')
            active_tab = ui.tab('👥 Active Probations', icon='pending_actions')
            new_tab = ui.tab('🚀 New Probation', icon='person_add')
            analytics_tab = ui.tab('📈 AI Analytics', icon='analytics')
            reports_tab = ui.tab('📋 Reports', icon='assessment')

        with ui.tab_panels(tabs, value=overview_tab).classes('w-full'):
            # Overview Panel - New modern dashboard
            with ui.tab_panel(overview_tab):
                create_probation_overview_section()
            
            # Active Probations Panel
            with ui.tab_panel(active_tab):
                create_active_probations_section()
            
            # New Probation Panel
            with ui.tab_panel(new_tab):
                create_new_probation_section()
            
            # AI Analytics Panel
            with ui.tab_panel(analytics_tab):
                create_smart_analytics_section()
            
            # Reports Panel
            with ui.tab_panel(reports_tab):
                create_probation_reports_section()

def create_probation_overview_section():
    """Create modern overview dashboard with visual metrics"""
    with ui.row().classes('w-full gap-6'):
        # Left column - Key metrics with modern cards
        with ui.column().classes('flex-1'):
            ui.label('📊 Performance Overview').classes('text-2xl font-bold text-gray-800 mb-4')
            
            # Metrics grid
            with ui.grid(columns=2).classes('w-full gap-4 mb-6'):
                # Success rate card
                with ui.card().classes('p-6 bg-gradient-to-br from-green-500 to-green-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">87%</div>
                                <div class="text-green-100">Success Rate</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">trending_up</i>
                        </div>
                    ''', sanitize=False)
                
                # Active probations card
                with ui.card().classes('p-6 bg-gradient-to-br from-blue-500 to-blue-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">12</div>
                                <div class="text-blue-100">Active Cases</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">groups</i>
                        </div>
                    ''', sanitize=False)
                
                # Average duration card
                with ui.card().classes('p-6 bg-gradient-to-br from-orange-500 to-orange-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">4.2</div>
                                <div class="text-orange-100">Avg Months</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">schedule</i>
                        </div>
                    ''', sanitize=False)
                
                # AI predictions card
                with ui.card().classes('p-6 bg-gradient-to-br from-purple-500 to-purple-600 text-white'):
                    ui.html('''
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="text-3xl font-bold">94%</div>
                                <div class="text-purple-100">AI Accuracy</div>
                            </div>
                            <i class="material-icons text-4xl opacity-75">psychology</i>
                        </div>
                    ''', sanitize=False)
            
            # Recent activity
            with ui.card().classes('p-6'):
                ui.label('🕒 Recent Activity').classes('text-xl font-semibold text-gray-800 mb-4')
                recent_activities = [
                    {"action": "Probation Completed", "employee": "Sarah Johnson", "time": "2 hours ago", "status": "success"},
                    {"action": "Review Scheduled", "employee": "Mike Chen", "time": "4 hours ago", "status": "pending"},
                    {"action": "Goals Updated", "employee": "Lisa Rodriguez", "time": "1 day ago", "status": "info"},
                    {"action": "Warning Issued", "employee": "James Wilson", "time": "2 days ago", "status": "warning"}
                ]
                
                for activity in recent_activities:
                    with ui.row().classes('w-full items-center justify-between p-3 hover:bg-gray-50 rounded-lg'):
                        with ui.row().classes('items-center gap-3'):
                            status_colors = {
                                'success': 'text-green-500',
                                'pending': 'text-blue-500',
                                'info': 'text-purple-500',
                                'warning': 'text-orange-500'
                            }
                            ui.icon('circle').classes(f'{status_colors[activity["status"]]} text-xs')
                            with ui.column().classes('gap-1'):
                                ui.label(activity['action']).classes('font-medium text-gray-800')
                                ui.label(activity['employee']).classes('text-sm text-gray-600')
                        ui.label(activity['time']).classes('text-xs text-gray-500')
        
        # Right column - AI insights and charts
        with ui.column().classes('flex-1'):
            ui.label('🧠 AI Insights').classes('text-2xl font-bold text-gray-800 mb-4')
            
            # AI recommendation card
            with ui.card().classes('p-6 bg-gradient-to-br from-indigo-50 to-purple-50 border-l-4 border-purple-500 mb-6'):
                ui.html('''
                    <div class="flex items-start gap-4">
                        <div class="bg-purple-500 text-white p-2 rounded-full">
                            <i class="material-icons">lightbulb</i>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold text-purple-800 mb-2">Today's AI Recommendation</h3>
                            <p class="text-purple-700 mb-3">Consider scheduling early review for Mike Chen based on improved performance metrics (confidence: 92%)</p>
                            <button class="bg-purple-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-purple-600">
                                View Details
                            </button>
                        </div>
                    </div>
                ''', sanitize=False)
            
            # Performance trends
            with ui.card().classes('p-6'):
                ui.label('📈 Performance Trends').classes('text-xl font-semibold text-gray-800 mb-4')
                ui.html('''
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Communication Skills</span>
                            <span class="text-sm text-green-600">↗ +15%</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-green-500 h-2 rounded-full" style="width: 78%"></div>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Technical Performance</span>
                            <span class="text-sm text-blue-600">↗ +8%</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-blue-500 h-2 rounded-full" style="width: 65%"></div>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Time Management</span>
                            <span class="text-sm text-orange-600">→ 0%</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-orange-500 h-2 rounded-full" style="width: 45%"></div>
                        </div>
                        
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-600">Team Collaboration</span>
                            <span class="text-sm text-purple-600">↗ +22%</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-purple-500 h-2 rounded-full" style="width: 82%"></div>
                        </div>
                    </div>
                ''', sanitize=False)

def create_smart_dashboard():
    """Create smart dashboard with key metrics"""
    with ui.row().classes('w-full gap-4 mb-6'):
        # Smart metrics cards with gradients
        with ui.card().classes('p-6 bg-gradient-to-r from-purple-500 to-purple-600 text-white min-w-48'):
            ui.html('''
                <div class="flex justify-between items-center">
                    <div>
                        <div class="text-2xl font-bold">12</div>
                        <div class="text-purple-100">Active Probations</div>
                    </div>
                    <i class="material-icons text-3xl opacity-75">groups</i>
                </div>
            ''', sanitize=False)
        
        with ui.card().classes('p-6 bg-gradient-to-r from-green-500 to-green-600 text-white min-w-48'):
            ui.html('''
                <div class="flex justify-between items-center">
                    <div>
                        <div class="text-2xl font-bold">87%</div>
                        <div class="text-green-100">Success Rate</div>
                    </div>
                    <i class="material-icons text-3xl opacity-75">trending_up</i>
                </div>
            ''', sanitize=False)
        
        with ui.card().classes('p-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white min-w-48'):
            ui.html('''
                <div class="flex justify-between items-center">
                    <div>
                        <div class="text-2xl font-bold">94%</div>
                        <div class="text-blue-100">AI Accuracy</div>
                    </div>
                    <i class="material-icons text-3xl opacity-75">psychology</i>
                </div>
            ''', sanitize=False)

def create_probation_analytics_dashboard():
    """Create intelligent probation analytics dashboard"""
    analytics = probation_manager.get_probation_analytics()
    
    with ui.row().classes('w-full gap-4 mb-6'):
        # Active Probations Card
        with ui.card().classes('p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Active Probations').classes('text-blue-100 text-sm')
                    ui.label(f'{analytics["total_active"]}').classes('text-2xl font-bold')
                ui.icon('hourglass_empty').classes('text-3xl text-blue-200')
        
        # High Risk Probations Card
        with ui.card().classes('p-4 bg-gradient-to-r from-red-500 to-red-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('High Risk Cases').classes('text-red-100 text-sm')
                    ui.label(f'{analytics["risk_distribution"]["High"]}').classes('text-2xl font-bold')
                ui.icon('warning').classes('text-3xl text-red-200')
        
        # Average Performance Card
        with ui.card().classes('p-4 bg-gradient-to-r from-green-500 to-green-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Avg Performance').classes('text-green-100 text-sm')
                    ui.label(f'{analytics["average_score"]:.1f}%').classes('text-2xl font-bold')
                ui.icon('trending_up').classes('text-3xl text-green-200')
        
        # Overdue Reviews Card
        with ui.card().classes('p-4 bg-gradient-to-r from-orange-500 to-orange-600 text-white min-w-48'):
            with ui.row().classes('items-center justify-between'):
                with ui.column():
                    ui.label('Overdue Reviews').classes('text-orange-100 text-sm')
                    ui.label(f'{analytics["overdue_reviews"]}').classes('text-2xl font-bold')
                ui.icon('schedule').classes('text-3xl text-orange-200')

def create_active_probations_section():
    """Create active probations management section with smart insights"""
    with ui.card().classes('w-full p-6'):
        ui.label('Active Probation Cases').classes('text-xl font-semibold mb-4')
        
        active_probations = [r for r in probation_manager.probation_records if r['status'] == 'Active']
        
        if not active_probations:
            with ui.column().classes('items-center py-8'):
                ui.icon('check_circle').classes('text-green-400 text-6xl mb-4')
                ui.label('No active probation cases').classes('text-gray-500 text-lg')
                ui.label('All employees have completed their probation periods').classes('text-gray-400 text-sm')
        else:
            # Smart table with AI insights
            with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
                ui.label('Probation ID').classes('w-28')
                ui.label('Employee').classes('flex-1')
                ui.label('Type').classes('w-32')
                ui.label('Progress').classes('w-24 text-center')
                ui.label('Performance').classes('w-24 text-center')
                ui.label('Risk Level').classes('w-24 text-center')
                ui.label('Next Review').classes('w-28')
                ui.label('Actions').classes('w-32 text-center')
            
            for record in active_probations:
                probation_config = probation_manager.probation_types.get(record['probation_type'], {})
                color = probation_config.get('color', 'blue')
                
                risk_color = 'text-red-600' if record['risk_level'] == 'High' else 'text-yellow-600' if record['risk_level'] == 'Medium' else 'text-green-600'
                
                with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50'):
                    ui.label(record['id']).classes('w-28 font-mono text-sm')
                    
                    with ui.column().classes('flex-1'):
                        ui.label(record['employee_name']).classes('font-medium')
                        ui.label(f'Started: {record["start_date"]}').classes('text-sm text-gray-500')
                    
                    ui.chip(record['probation_type'], color=color).props('dense').classes('w-32')
                    
                    # Progress bar
                    progress = record.get('completion_percentage', 0)
                    progress_color = 'text-green-600' if progress >= 75 else 'text-yellow-600' if progress >= 50 else 'text-red-600'
                    ui.label(f'{progress}%').classes(f'w-24 text-center font-bold {progress_color}')
                    
                    # Performance score
                    score = record.get('current_score', 0)
                    score_color = 'text-green-600' if score >= 80 else 'text-yellow-600' if score >= 70 else 'text-red-600'
                    ui.label(f'{score}%').classes(f'w-24 text-center font-bold {score_color}')
                    
                    # Risk level
                    ui.label(record['risk_level']).classes(f'w-24 text-center font-bold {risk_color}')
                    
                    # Next review date
                    next_review = datetime.strptime(record['next_review_date'], '%Y-%m-%d').date()
                    overdue = next_review < date.today()
                    review_color = 'text-red-600' if overdue else 'text-gray-700'
                    ui.label(record['next_review_date']).classes(f'w-28 text-sm {review_color}')
                    
                    with ui.row().classes('w-32 justify-center gap-1'):
                        ui.button(icon='visibility', on_click=lambda r=record: view_probation_details(r)).props('size=sm flat color=blue')
                        ui.button(icon='edit', on_click=lambda r=record: edit_probation_record(r)).props('size=sm flat color=green')
                        ui.button(icon='psychology', on_click=lambda r=record: show_ai_insights(r)).props('size=sm flat color=purple')

def create_new_probation_section():
    """Create new probation form with smart suggestions"""
    with ui.card().classes('w-full p-6'):
        ui.label('Create New Probation Record').classes('text-xl font-semibold mb-4')
        
        with ui.row().classes('w-full gap-6'):
            # Left column - Employee Selection
            with ui.column().classes('flex-1'):
                ui.label('Employee Information').classes('font-semibold text-lg text-blue-600 mb-3')
                
                # Employee selection with smart filtering
                eligible_employees = [f"{emp['id']} - {emp['name']} ({emp['department']})" for emp in probation_manager.employees]
                employee_select = ui.select(options=eligible_employees, label='Select Employee').props('outlined').classes('w-full mb-3')
                
                # Employee info display
                employee_info_display = ui.element('div').classes('p-3 border rounded-lg mb-3 bg-gray-50')
                
                # Probation type selection
                probation_types = list(probation_manager.probation_types.keys())
                probation_type_select = ui.select(options=probation_types, label='Probation Type').props('outlined').classes('w-full mb-3')
                
                ui.label('Start Date').classes('text-sm font-medium text-gray-700 mb-1')
                start_date_input = ui.date(value=date.today()).props('outlined').classes('w-full mb-3')
                
                reason_input = ui.textarea('Reason for Probation', 
                    placeholder='Explain the reason for placing employee on probation...'
                ).props('outlined rows=3').classes('w-full mb-3')
                
            # Right column - Smart Configuration
            with ui.column().classes('flex-1'):
                ui.label('Smart Configuration').classes('font-semibold text-lg text-purple-600 mb-3')
                
                # Probation details display
                probation_details_display = ui.element('div').classes('p-3 border rounded-lg mb-3')
                
                # AI recommendations display
                ai_recommendations_display = ui.element('div').classes('p-3 border rounded-lg mb-3 bg-blue-50')
                
                # Initial goals setting
                ui.label('Initial Performance Goals').classes('font-semibold text-green-600 mb-2')
                goals_input = ui.textarea('Performance Goals', 
                    placeholder='List specific, measurable goals for this probation period...'
                ).props('outlined rows=4').classes('w-full mb-3')
                
                # Success metrics
                ui.label('Success Metrics').classes('font-semibold text-orange-600 mb-2')
                for metric, details in probation_manager.performance_metrics.items():
                    with ui.row().classes('items-center gap-2 mb-1'):
                        ui.checkbox(metric).classes('text-sm')
                        ui.label(f'({details["weight"]}%)').classes('text-xs text-gray-500')
        
        # Smart recommendations preview
        with ui.row().classes('w-full p-4 bg-gray-50 rounded-lg mb-4'):
            ui.label('🧠 AI-Powered Recommendations').classes('font-semibold text-gray-700')
            recommendations_preview = ui.label('Select employee and probation type for personalized recommendations').classes('text-purple-600 ml-4')
        
        # Update recommendations when selections change
        def update_smart_recommendations():
            if employee_select.value and probation_type_select.value:
                # Extract employee ID from selection
                employee_id = employee_select.value.split(' - ')[0]
                employee = next((emp for emp in probation_manager.employees if emp["id"] == employee_id), None)
                
                if employee:
                    # Update employee info display
                    employee_info_display.clear()
                    with employee_info_display:
                        ui.label('Employee Profile').classes('font-semibold text-blue-600 mb-2')
                        ui.label(f'Department: {employee.get("department")}').classes('text-sm')
                        ui.label(f'Position: {employee.get("position")}').classes('text-sm')
                        ui.label(f'Start Date: {employee.get("start_date")}').classes('text-sm')
                        ui.label(f'Manager: {employee.get("manager_name")}').classes('text-sm')
                        ui.label(f'New Hire: {"Yes" if employee.get("is_new_hire") else "No"}').classes('text-sm')
                    
                    # Update probation configuration
                    probation_config = probation_manager.probation_types.get(probation_type_select.value, {})
                    probation_details_display.clear()
                    with probation_details_display:
                        ui.label('Probation Configuration').classes('font-semibold text-green-600 mb-2')
                        ui.label(f'Duration: {probation_config.get("duration_months", 0)} months').classes('text-sm')
                        ui.label(f'Review Intervals: {", ".join(map(str, probation_config.get("review_intervals", [])))} months').classes('text-sm')
                        ui.label(f'Performance Threshold: {probation_config.get("performance_threshold", 0)}%').classes('text-sm')
                        ui.label(f'Extensions Allowed: {"Yes" if probation_config.get("auto_extension_allowed") else "No"}').classes('text-sm')
                    
                    # Generate AI recommendations
                    ai_recommendations_display.clear()
                    with ai_recommendations_display:
                        ui.label('🤖 AI Recommendations').classes('font-semibold text-purple-600 mb-2')
                        
                        # Mock AI recommendations based on employee and probation type
                        if employee.get("is_new_hire") and probation_type_select.value == "Initial Probation":
                            ui.label('• Schedule weekly check-ins for first month').classes('text-sm text-blue-700')
                            ui.label('• Assign buddy/mentor for orientation support').classes('text-sm text-blue-700')
                            ui.label('• Focus on job knowledge and company culture').classes('text-sm text-blue-700')
                        elif probation_type_select.value == "Performance Improvement":
                            ui.label('• Implement daily performance monitoring').classes('text-sm text-red-700')
                            ui.label('• Provide additional training resources').classes('text-sm text-red-700')
                            ui.label('• Set clear, measurable improvement targets').classes('text-sm text-red-700')
        
        # Bind recommendation updates
        employee_select.on('update:model-value', lambda: update_smart_recommendations())
        probation_type_select.on('update:model-value', lambda: update_smart_recommendations())
        
        # Action buttons
        with ui.row().classes('w-full justify-end gap-2 mt-6'):
            ui.button('Generate Smart Goals', on_click=lambda: generate_smart_goals(
                employee_select.value, probation_type_select.value
            )).props('flat color=purple')
            ui.button('Create Probation', on_click=lambda: submit_probation_record(
                employee_select.value, probation_type_select.value, start_date_input.value,
                reason_input.value, goals_input.value
            )).props('color=primary')

def create_performance_reviews_section():
    """Create performance review management section"""
    with ui.card().classes('w-full p-6'):
        ui.label('📊 Performance Review Center').classes('text-xl font-semibold mb-4')
        
        # Mock performance review data
        reviews = [
            {
                "id": "REV-001",
                "probation_id": "PROB-001",
                "employee_name": "Alice Johnson",
                "review_date": "2024-09-01",
                "reviewer": "David Thompson",
                "overall_score": 78,
                "categories": {
                    "Job Knowledge": 80,
                    "Quality of Work": 75,
                    "Productivity": 78,
                    "Communication": 82,
                    "Teamwork": 75,
                    "Initiative": 70
                },
                "status": "Completed"
            },
            {
                "id": "REV-002", 
                "probation_id": "PROB-002",
                "employee_name": "Robert Chen",
                "review_date": "2024-08-15",
                "reviewer": "Michael Chen",
                "overall_score": 65,
                "categories": {
                    "Job Knowledge": 60,
                    "Quality of Work": 65,
                    "Productivity": 70,
                    "Communication": 68,
                    "Teamwork": 72,
                    "Initiative": 55
                },
                "status": "Completed"
            }
        ]
        
        # Reviews table
        with ui.row().classes('w-full p-4 bg-gray-50 rounded-t-lg font-semibold'):
            ui.label('Review ID').classes('w-24')
            ui.label('Employee').classes('flex-1')
            ui.label('Review Date').classes('w-28')
            ui.label('Reviewer').classes('w-32')
            ui.label('Overall Score').classes('w-28 text-center')
            ui.label('Status').classes('w-24')
            ui.label('Actions').classes('w-24 text-center')
        
        for review in reviews:
            score_color = 'text-green-600' if review['overall_score'] >= 80 else 'text-yellow-600' if review['overall_score'] >= 70 else 'text-red-600'
            
            with ui.row().classes('w-full p-4 border-b border-gray-200 hover:bg-gray-50'):
                ui.label(review['id']).classes('w-24 font-mono text-sm')
                ui.label(review['employee_name']).classes('flex-1 font-medium')
                ui.label(review['review_date']).classes('w-28 text-sm')
                ui.label(review['reviewer']).classes('w-32 text-sm')
                ui.label(f"{review['overall_score']}%").classes(f'w-28 text-center font-bold {score_color}')
                ui.chip(review['status'], color='green').props('dense').classes('w-24')
                ui.button(icon='visibility', on_click=lambda r=review: view_review_details(r)).props('size=sm flat color=blue').classes('w-24')

def create_smart_analytics_section():
    """Create AI-powered analytics section"""
    with ui.card().classes('w-full p-6'):
        ui.label('🤖 AI-Powered Analytics & Insights').classes('text-xl font-semibold mb-4')
        
        with ui.row().classes('w-full gap-6'):
            # Success prediction
            with ui.card().classes('flex-1 p-4'):
                ui.label('Success Prediction Model').classes('font-semibold text-green-600 mb-3')
                
                # Mock predictions for active probations
                predictions = [
                    {"name": "Alice Johnson", "success_rate": 85, "confidence": 92},
                    {"name": "Robert Chen", "success_rate": 45, "confidence": 78},
                    {"name": "Maria Garcia", "success_rate": 72, "confidence": 85}
                ]
                
                for pred in predictions:
                    with ui.row().classes('justify-between items-center mb-2'):
                        ui.label(pred["name"]).classes('text-sm font-medium')
                        success_color = 'text-green-600' if pred["success_rate"] >= 70 else 'text-yellow-600' if pred["success_rate"] >= 50 else 'text-red-600'
                        ui.label(f'{pred["success_rate"]}%').classes(f'font-bold {success_color}')
                    
                    # Confidence indicator
                    ui.label(f'Confidence: {pred["confidence"]}%').classes('text-xs text-gray-500 mb-2')
            
            # Risk factors analysis
            with ui.card().classes('flex-1 p-4'):
                ui.label('Risk Factors Analysis').classes('font-semibold text-red-600 mb-3')
                
                risk_factors = [
                    {"factor": "Below Performance Threshold", "impact": "High", "frequency": 1},
                    {"factor": "Missed Review Deadlines", "impact": "Medium", "frequency": 0},
                    {"factor": "Poor Goal Achievement", "impact": "High", "frequency": 2},
                    {"factor": "Manager Concerns", "impact": "Medium", "frequency": 1}
                ]
                
                for factor in risk_factors:
                    impact_color = 'text-red-600' if factor["impact"] == "High" else 'text-yellow-600'
                    with ui.row().classes('justify-between items-center mb-2'):
                        ui.label(factor["factor"]).classes('text-sm')
                        with ui.row().classes('items-center gap-2'):
                            ui.label(str(factor["frequency"])).classes('font-bold')
                            ui.chip(factor["impact"], color='red' if factor["impact"] == "High" else 'yellow').props('dense size=sm')

def create_probation_policies_section():
    """Create probation policies and procedures"""
    with ui.card().classes('w-full p-6'):
        ui.label('📋 Probation Policies & Procedures').classes('text-xl font-semibold mb-4')
        
        for probation_type, config in probation_manager.probation_types.items():
            with ui.expansion(probation_type, icon='policy').classes('w-full mb-2'):
                with ui.column().classes('p-4'):
                    with ui.grid(columns=2).classes('gap-4'):
                        # Left column
                        with ui.column():
                            ui.label('Policy Configuration').classes('font-semibold text-blue-600 mb-2')
                            ui.label(f'Code: {config["code"]}').classes('text-sm mb-1')
                            ui.label(f'Duration: {config["duration_months"]} months').classes('text-sm mb-1')
                            ui.label(f'Performance Threshold: {config["performance_threshold"]}%').classes('text-sm mb-1')
                            ui.label(f'Extensions Allowed: {"Yes" if config["auto_extension_allowed"] else "No"}').classes('text-sm mb-1')
                            ui.label(f'Max Extensions: {config["max_extensions"]}').classes('text-sm mb-1')
                        
                        # Right column
                        with ui.column():
                            ui.label('Review Schedule').classes('font-semibold text-green-600 mb-2')
                            ui.label('Review Intervals:').classes('text-sm font-medium mb-1')
                            for interval in config["review_intervals"]:
                                ui.label(f'• Month {interval}').classes('text-sm text-gray-700')

# Action functions with smart algorithms
async def submit_probation_record(employee_selection, probation_type, start_date, reason, goals):
    """Submit probation record with AI validation"""
    if not all([employee_selection, probation_type, start_date, reason]):
        ui.notify('Please fill in all required fields', color='negative')
        return
    
    # Extract employee information
    employee_id = employee_selection.split(' - ')[0]
    employee_name = employee_selection.split(' - ')[1].split(' (')[0]
    
    probation_data = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "probation_type": probation_type,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "reason": reason,
        "initial_goals": goals
    }
    
    success, record_id = probation_manager.create_probation_record(probation_data)
    
    if success:
        ui.notify(f'Probation record created successfully! ID: {record_id}', color='positive')
        
        # Show AI insights dialog
        with ui.dialog() as dialog, ui.card().classes('w-96 p-6'):
            ui.label('🤖 Probation Created Successfully').classes('text-xl font-semibold mb-4 text-blue-600')
            ui.label(f'Record ID: {record_id}').classes('font-mono text-sm mb-2')
            
            # Generate initial AI recommendations
            mock_record = {"probation_type": probation_type, "current_score": 60, "goals_set": 3, "goals_achieved": 0}
            recommendations = probation_manager.generate_smart_recommendations(mock_record)
            
            if recommendations:
                ui.label('AI Recommendations:').classes('font-semibold mb-2')
                for rec in recommendations[:3]:  # Show top 3
                    ui.label(f'• {rec["action"]}').classes('text-sm text-blue-600 mb-1')
            
            ui.label('Smart monitoring activated').classes('text-green-600 text-sm mt-4')
            ui.button('OK', on_click=dialog.close).props('color=primary')
        
        dialog.open()
    else:
        ui.notify('Error creating probation record', color='negative')

async def generate_smart_goals(employee_selection, probation_type):
    """Generate AI-powered SMART goals"""
    if not employee_selection or not probation_type:
        ui.notify('Please select employee and probation type first', color='warning')
        return
    
    # Mock AI-generated goals
    goals_templates = {
        "Initial Probation": [
            "Complete departmental orientation training within 2 weeks",
            "Achieve 75% score on role-specific competency assessment by month 3",
            "Establish effective working relationships with 5 key team members",
            "Demonstrate proficiency in core job functions by month 6"
        ],
        "Performance Improvement": [
            "Improve performance rating from current level to 80% within 3 months",
            "Complete remedial training in identified weak areas within 4 weeks",
            "Achieve zero customer complaints for 2 consecutive months",
            "Meet all project deadlines for the probation period"
        ]
    }
    
    suggested_goals = goals_templates.get(probation_type, ["Standard performance goals to be defined"])
    
    with ui.dialog() as dialog, ui.card().classes('w-[500px] p-6'):
        ui.label('🎯 AI-Generated SMART Goals').classes('text-xl font-semibold mb-4')
        
        ui.label('Suggested goals for this probation:').classes('font-medium mb-3')
        for i, goal in enumerate(suggested_goals, 1):
            ui.label(f'{i}. {goal}').classes('text-sm mb-2 p-2 bg-blue-50 rounded')
        
        ui.label('These goals are generated based on probation type and best practices').classes('text-gray-500 text-sm mt-4')
        ui.button('Use These Goals', on_click=dialog.close).props('color=primary').classes('w-full mt-4')
    
    dialog.open()

async def view_probation_details(record):
    """View detailed probation information with AI insights"""
    with ui.dialog() as dialog, ui.card().classes('w-[700px] p-6'):
        ui.label(f'Probation Details - {record["id"]}').classes('text-xl font-semibold mb-4')
        
        with ui.grid(columns=2).classes('gap-4 w-full'):
            # Left column
            with ui.column().classes('gap-3'):
                ui.label('Probation Information').classes('font-semibold text-blue-600')
                ui.label(f'Employee: {record["employee_name"]}').classes('text-sm')
                ui.label(f'Type: {record["probation_type"]}').classes('text-sm')
                ui.label(f'Start Date: {record["start_date"]}').classes('text-sm')
                ui.label(f'End Date: {record["end_date"]}').classes('text-sm')
                ui.label(f'Status: {record["status"]}').classes('text-sm')
                ui.label(f'Next Review: {record["next_review_date"]}').classes('text-sm')
            
            # Right column
            with ui.column().classes('gap-3'):
                ui.label('Performance Metrics').classes('font-semibold text-green-600')
                ui.label(f'Current Score: {record["current_score"]}%').classes('text-sm')
                ui.label(f'Progress: {record["completion_percentage"]}%').classes('text-sm')
                ui.label(f'Goals Set: {record["goals_set"]}').classes('text-sm')
                ui.label(f'Goals Achieved: {record["goals_achieved"]}').classes('text-sm')
                ui.label(f'Risk Level: {record["risk_level"]}').classes('text-sm')
        
        # AI recommendations
        if record.get("smart_recommendations"):
            ui.label('AI Recommendations:').classes('font-semibold text-purple-600 mt-4')
            for rec in record["smart_recommendations"]:
                ui.label(f'• {rec}').classes('text-sm text-purple-500 ml-4')
        
        # Success prediction
        success_rate = probation_manager.predict_probation_success(record)
        ui.label(f'Success Prediction: {success_rate:.1f}%').classes('font-semibold text-blue-600 mt-4')
        
        with ui.row().classes('w-full justify-end mt-6'):
            ui.button('Close', on_click=dialog.close).props('flat')
    
    dialog.open()

async def edit_probation_record(record):
    """Edit probation record with smart suggestions"""
    ui.notify(f'Edit probation {record["id"]} - Smart editing interface coming soon!', color='info')

async def show_ai_insights(record):
    """Show AI-powered insights for probation record"""
    with ui.dialog() as dialog, ui.card().classes('w-[600px] p-6'):
        ui.label(f'🤖 AI Insights - {record["employee_name"]}').classes('text-xl font-semibold mb-4')
        
        # Performance trend analysis
        ui.label('Performance Trend Analysis').classes('font-semibold text-blue-600 mb-2')
        ui.label('📈 Showing steady improvement in communication skills').classes('text-sm text-green-600 mb-1')
        ui.label('⚠️ Technical competency needs attention').classes('text-sm text-yellow-600 mb-1')
        ui.label('🎯 Goal achievement rate below expectations').classes('text-sm text-red-600 mb-4')
        
        # Risk assessment
        ui.label('Risk Assessment').classes('font-semibold text-red-600 mb-2')
        risk_score = 35  # Mock calculation
        risk_color = 'text-red-600' if risk_score >= 60 else 'text-yellow-600' if risk_score >= 30 else 'text-green-600'
        ui.label(f'Risk Score: {risk_score}% - {record["risk_level"]} Risk').classes(f'text-sm {risk_color} mb-4')
        
        # Recommendations
        ui.label('Smart Recommendations').classes('font-semibold text-purple-600 mb-2')
        recommendations = probation_manager.generate_smart_recommendations(record)
        for rec in recommendations[:3]:
            priority_color = 'text-red-600' if rec['priority'] == 'High' else 'text-yellow-600' if rec['priority'] == 'Medium' else 'text-green-600'
            ui.label(f'[{rec["priority"]}] {rec["action"]}').classes(f'text-sm {priority_color} mb-1')
        
        # Success prediction
        success_rate = probation_manager.predict_probation_success(record)
        success_color = 'text-green-600' if success_rate >= 70 else 'text-yellow-600' if success_rate >= 50 else 'text-red-600'
        ui.label(f'Success Probability: {success_rate:.1f}%').classes(f'font-semibold {success_color} mt-4')
        
        ui.button('Close', on_click=dialog.close).props('color=primary').classes('w-full mt-4')
    
    dialog.open()

async def view_review_details(review):
    """View detailed performance review"""
    with ui.dialog() as dialog, ui.card().classes('w-[600px] p-6'):
        ui.label(f'Performance Review - {review["employee_name"]}').classes('text-xl font-semibold mb-4')
        
        ui.label(f'Review Date: {review["review_date"]}').classes('text-sm mb-2')
        ui.label(f'Reviewer: {review["reviewer"]}').classes('text-sm mb-4')
        
        ui.label('Category Scores:').classes('font-semibold mb-2')
        for category, score in review["categories"].items():
            score_color = 'text-green-600' if score >= 80 else 'text-yellow-600' if score >= 70 else 'text-red-600'
            with ui.row().classes('justify-between mb-1'):
                ui.label(category).classes('text-sm')
                ui.label(f'{score}%').classes(f'text-sm font-bold {score_color}')
        
        overall_color = 'text-green-600' if review["overall_score"] >= 80 else 'text-yellow-600' if review["overall_score"] >= 70 else 'text-red-600'
        ui.label(f'Overall Score: {review["overall_score"]}%').classes(f'font-semibold {overall_color} mt-4')
        
        ui.button('Close', on_click=dialog.close).props('color=primary').classes('w-full mt-4')
    
    dialog.open()

async def show_performance_analytics():
    """Show performance analytics dashboard"""
    ui.notify('Advanced performance analytics dashboard - Feature coming soon!', color='info')



# Integration APIs with AI capabilities
def get_probation_recommendations(employee_id):
    """API to get AI recommendations for specific employee"""
    record = next((r for r in probation_manager.probation_records if r["employee_id"] == employee_id), None)
    if record:
        return probation_manager.generate_smart_recommendations(record)
    return []

def predict_probation_outcomes():
    """API to get success predictions for all active probations"""
    active_records = [r for r in probation_manager.probation_records if r["status"] == "Active"]
    predictions = []
    
    for record in active_records:
        success_rate = probation_manager.predict_probation_success(record)
        predictions.append({
            "employee_id": record["employee_id"],
            "employee_name": record["employee_name"],
            "success_probability": success_rate,
            "risk_level": record["risk_level"]
        })
    
    return predictions

# Modern dialog functions
async def show_ai_analytics_dialog():
    """Show AI analytics dialog with advanced insights"""
    with ui.dialog() as dialog, ui.card().classes('w-4xl max-w-4xl p-8'):
        ui.html('''
            <div class="flex items-center gap-3 mb-6">
                <div class="bg-purple-500 text-white p-3 rounded-full">
                    <i class="material-icons text-2xl">psychology</i>
                </div>
                <div>
                    <h2 class="text-2xl font-bold text-purple-800">AI Analytics Dashboard</h2>
                    <p class="text-purple-600">Advanced machine learning insights and predictions</p>
                </div>
            </div>
        ''', sanitize=False)
        
        with ui.row().classes('w-full gap-6'):
            # Left column - Predictions
            with ui.column().classes('flex-1'):
                ui.label('🔮 AI Predictions').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4 bg-gradient-to-br from-blue-50 to-indigo-50 border-l-4 border-blue-500'):
                    ui.html('''
                        <div class="space-y-3">
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Success Probability</span>
                                <span class="text-green-600 font-bold">87%</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Completion Timeline</span>
                                <span class="text-blue-600 font-bold">4.2 months</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="font-medium">Risk Factor</span>
                                <span class="text-orange-600 font-bold">Low</span>
                            </div>
                        </div>
                    ''', sanitize=False)
            
            # Right column - Recommendations
            with ui.column().classes('flex-1'):
                ui.label('💡 Smart Recommendations').classes('text-xl font-semibold text-gray-800 mb-4')
                with ui.card().classes('p-4 bg-gradient-to-br from-green-50 to-emerald-50 border-l-4 border-green-500'):
                    ui.html('''
                        <div class="space-y-2">
                            <div class="text-sm font-medium text-green-800">• Schedule weekly check-ins</div>
                            <div class="text-sm font-medium text-green-800">• Focus on communication skills</div>
                            <div class="text-sm font-medium text-green-800">• Provide mentorship program</div>
                            <div class="text-sm font-medium text-green-800">• Set measurable goals</div>
                        </div>
                    ''', sanitize=False)
        
        ui.button('Close', on_click=dialog.close).props('flat color=purple').classes('mt-6')
    dialog.open()

async def show_new_probation_dialog():
    """Show new probation creation dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-3xl max-w-3xl p-8'):
        ui.html('''
            <div class="flex items-center gap-3 mb-6">
                <div class="bg-indigo-500 text-white p-3 rounded-full">
                    <i class="material-icons text-2xl">person_add</i>
                </div>
                <div>
                    <h2 class="text-2xl font-bold text-indigo-800">Create New Probation</h2>
                    <p class="text-indigo-600">Initiate employee probation with AI assistance</p>
                </div>
            </div>
        ''', sanitize=False)
        
        # Quick probation form
        with ui.row().classes('w-full gap-4 mb-4'):
            employee_select = ui.select(['EMP-001 - John Smith', 'EMP-002 - Sarah Johnson'], 
                label='Select Employee').classes('flex-1')
            probation_type = ui.select(['Performance Improvement', 'Behavioral Issues', 'Skills Development'], 
                label='Probation Type').classes('flex-1')
        
        duration_input = ui.number('Duration (months)', value=3, min=1, max=12).classes('w-full mb-4')
        reason_input = ui.textarea('Reason', placeholder='Explain the reason for probation...').props('rows=3').classes('w-full mb-4')
        
        with ui.row().classes('gap-2 justify-end'):
            ui.button('Cancel', on_click=dialog.close).props('flat')
            ui.button('Create Probation', on_click=lambda: [ui.notify('Probation created successfully!', color='positive'), dialog.close()]).props('color=indigo')
    
    dialog.open()

def create_probation_reports_section():
    """Create probation reports section with modern dashboard"""
    with ui.column().classes('w-full space-y-6'):
        # Header
        ui.html('''
            <div class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6 rounded-lg mb-6">
                <div class="flex items-center gap-3">
                    <i class="material-icons text-3xl">assessment</i>
                    <div>
                        <h2 class="text-2xl font-bold">Probation Reports</h2>
                        <p class="text-indigo-100">Comprehensive analytics and reports</p>
                    </div>
                </div>
            </div>
        ''', sanitize=False)
        
        # Quick report cards
        with ui.row().classes('w-full gap-4 mb-6'):
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-green-50 to-green-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-green-600 mb-2">trending_up</i>
                        <div class="text-2xl font-bold text-green-800">89%</div>
                        <div class="text-green-700">Success Rate</div>
                    </div>
                ''', sanitize=False)
            
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-blue-50 to-blue-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-blue-600 mb-2">schedule</i>
                        <div class="text-2xl font-bold text-blue-800">3.8</div>
                        <div class="text-blue-700">Avg Duration (months)</div>
                    </div>
                ''', sanitize=False)
            
            with ui.card().classes('p-6 flex-1 bg-gradient-to-br from-purple-50 to-purple-100'):
                ui.html('''
                    <div class="text-center">
                        <i class="material-icons text-4xl text-purple-600 mb-2">groups</i>
                        <div class="text-2xl font-bold text-purple-800">47</div>
                        <div class="text-purple-700">Total Cases</div>
                    </div>
                ''', sanitize=False)
        
        # Report generation
        with ui.card().classes('p-6'):
            ui.label('Generate Reports').classes('text-xl font-semibold text-gray-800 mb-4')
            
            with ui.row().classes('w-full gap-4 mb-4'):
                ui.select(['Monthly Summary', 'Quarterly Analysis', 'Annual Review', 'Custom Range'], 
                    label='Report Type').classes('flex-1')
                ui.select(['All Departments', 'HR', 'IT', 'Sales', 'Marketing'], 
                    label='Department').classes('flex-1')
            
            with ui.row().classes('gap-2'):
                ui.button('📊 Generate Report', on_click=lambda: ui.notify('Report generation started!', color='positive')).props('color=indigo')
                ui.button('📤 Export Data', on_click=lambda: ui.notify('Data export initiated!', color='info')).props('outlined')
                ui.button('📧 Email Report', on_click=lambda: ui.notify('Report will be emailed!', color='blue')).props('outlined')