package com.dpk.CareerGuidance.Model;

import java.util.List;

public class IndianEducationStream {
    private String streamName;
    private String level; // 10th, 12th, UG, PG
    private List<String> subjects;
    private List<String> commonExams;
    private List<String> careerOptions;
    private List<String> topColleges;
    private String description;

    // Constructors
    public IndianEducationStream() {}

    public IndianEducationStream(String streamName, String level) {
        this.streamName = streamName;
        this.level = level;
    }

    // Getters and Setters
    public String getStreamName() { return streamName; }
    public void setStreamName(String streamName) { this.streamName = streamName; }

    public String getLevel() { return level; }
    public void setLevel(String level) { this.level = level; }

    public List<String> getSubjects() { return subjects; }
    public void setSubjects(List<String> subjects) { this.subjects = subjects; }

    public List<String> getCommonExams() { return commonExams; }
    public void setCommonExams(List<String> commonExams) { this.commonExams = commonExams; }

    public List<String> getCareerOptions() { return careerOptions; }
    public void setCareerOptions(List<String> careerOptions) { this.careerOptions = careerOptions; }

    public List<String> getTopColleges() { return topColleges; }
    public void setTopColleges(List<String> topColleges) { this.topColleges = topColleges; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
