package com.dpk.CareerGuidance.Model;

import java.util.List;

public class CareerRecommendation {
    private String careerPath;
    private String description;
    private double matchPercentage;
    private List<String> requiredSkills;
    private List<String> recommendedExams;
    private List<String> suggestedCourses;
    private List<String> topColleges;
    private String expectedSalaryRange;
    private String jobMarketTrend;
    private List<String> alternativeCareers;
    private String roadmap;
    private List<String> skillGaps;
    private String reasoning;

    // Constructors
    public CareerRecommendation() {}

    public CareerRecommendation(String careerPath, String description, double matchPercentage) {
        this.careerPath = careerPath;
        this.description = description;
        this.matchPercentage = matchPercentage;
    }

    // Getters and Setters
    public String getCareerPath() { return careerPath; }
    public void setCareerPath(String careerPath) { this.careerPath = careerPath; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public double getMatchPercentage() { return matchPercentage; }
    public void setMatchPercentage(double matchPercentage) { this.matchPercentage = matchPercentage; }

    public List<String> getRequiredSkills() { return requiredSkills; }
    public void setRequiredSkills(List<String> requiredSkills) { this.requiredSkills = requiredSkills; }

    public List<String> getRecommendedExams() { return recommendedExams; }
    public void setRecommendedExams(List<String> recommendedExams) { this.recommendedExams = recommendedExams; }

    public List<String> getSuggestedCourses() { return suggestedCourses; }
    public void setSuggestedCourses(List<String> suggestedCourses) { this.suggestedCourses = suggestedCourses; }

    public List<String> getTopColleges() { return topColleges; }
    public void setTopColleges(List<String> topColleges) { this.topColleges = topColleges; }

    public String getExpectedSalaryRange() { return expectedSalaryRange; }
    public void setExpectedSalaryRange(String expectedSalaryRange) { this.expectedSalaryRange = expectedSalaryRange; }

    public String getJobMarketTrend() { return jobMarketTrend; }
    public void setJobMarketTrend(String jobMarketTrend) { this.jobMarketTrend = jobMarketTrend; }

    public List<String> getAlternativeCareers() { return alternativeCareers; }
    public void setAlternativeCareers(List<String> alternativeCareers) { this.alternativeCareers = alternativeCareers; }

    public String getRoadmap() { return roadmap; }
    public void setRoadmap(String roadmap) { this.roadmap = roadmap; }

    public List<String> getSkillGaps() { return skillGaps; }
    public void setSkillGaps(List<String> skillGaps) { this.skillGaps = skillGaps; }

    public String getReasoning() { return reasoning; }
    public void setReasoning(String reasoning) { this.reasoning = reasoning; }
}
