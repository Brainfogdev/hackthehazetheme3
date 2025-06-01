package com.dpk.CareerGuidance.Model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "student_profiles")
public class StudentProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String name;

    @NotNull
    private Integer age;

    @NotBlank
    private String currentClass; // 10th, 12th, Graduate, etc.

    @NotBlank
    private String currentStream; // Science, Commerce, Arts, Engineering, etc.

    @ElementCollection
    @CollectionTable(name = "student_subjects", joinColumns = @JoinColumn(name = "student_id"))
    @Column(name = "subject")
    private List<String> subjects;

    @ElementCollection
    @CollectionTable(name = "student_interests", joinColumns = @JoinColumn(name = "student_id"))
    @Column(name = "interest")
    private List<String> interests;

    @ElementCollection
    @CollectionTable(name = "student_skills", joinColumns = @JoinColumn(name = "student_id"))
    @Column(name = "skill")
    private List<String> skills;

    @ElementCollection
    @CollectionTable(name = "student_aspirations", joinColumns = @JoinColumn(name = "student_id"))
    @Column(name = "aspiration")
    private List<String> careerAspirations;

    private String academicPerformance; // Excellent, Good, Average, Below Average

    @ElementCollection
    @CollectionTable(name = "student_exam_scores", joinColumns = @JoinColumn(name = "student_id"))
    @MapKeyColumn(name = "exam_name")
    @Column(name = "score")
    private java.util.Map<String, Double> examScores; // JEE, NEET, CLAT, etc.

    private String location; // City, State

    private String familyBackground; // Business, Service, Agriculture, etc.

    private String economicStatus; // Upper, Middle, Lower

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // Constructors
    public StudentProfile() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public Integer getAge() { return age; }
    public void setAge(Integer age) { this.age = age; }

    public String getCurrentClass() { return currentClass; }
    public void setCurrentClass(String currentClass) { this.currentClass = currentClass; }

    public String getCurrentStream() { return currentStream; }
    public void setCurrentStream(String currentStream) { this.currentStream = currentStream; }

    public List<String> getSubjects() { return subjects; }
    public void setSubjects(List<String> subjects) { this.subjects = subjects; }

    public List<String> getInterests() { return interests; }
    public void setInterests(List<String> interests) { this.interests = interests; }

    public List<String> getSkills() { return skills; }
    public void setSkills(List<String> skills) { this.skills = skills; }

    public List<String> getCareerAspirations() { return careerAspirations; }
    public void setCareerAspirations(List<String> careerAspirations) { this.careerAspirations = careerAspirations; }

    public String getAcademicPerformance() { return academicPerformance; }
    public void setAcademicPerformance(String academicPerformance) { this.academicPerformance = academicPerformance; }

    public java.util.Map<String, Double> getExamScores() { return examScores; }
    public void setExamScores(java.util.Map<String, Double> examScores) { this.examScores = examScores; }

    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }

    public String getFamilyBackground() { return familyBackground; }
    public void setFamilyBackground(String familyBackground) { this.familyBackground = familyBackground; }

    public String getEconomicStatus() { return economicStatus; }
    public void setEconomicStatus(String economicStatus) { this.economicStatus = economicStatus; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }

    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}
