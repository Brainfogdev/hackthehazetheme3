package com.dpk.CareerGuidance.Controller;

import com.dpk.CareerGuidance.Model.CareerRecommendation;
import com.dpk.CareerGuidance.Model.IndianEducationStream;
import com.dpk.CareerGuidance.Model.StudentProfile;
import com.dpk.CareerGuidance.Service.CareerGuidanceService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/career")
@CrossOrigin(origins = "*")
public class CareerController {

    private static final Logger logger = LoggerFactory.getLogger(CareerController.class);

    private final CareerGuidanceService careerService;

    public CareerController(CareerGuidanceService careerService) {
        this.careerService = careerService;
    }

    @PostMapping("/profile")
    public ResponseEntity<StudentProfile> createStudentProfile(@Valid @RequestBody StudentProfile profile) {
        logger.info("Creating profile for student: {}", profile.getName());
        StudentProfile savedProfile = careerService.saveStudentProfile(profile);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedProfile);
    }

    @GetMapping("/profile/{id}")
    public ResponseEntity<StudentProfile> getStudentProfile(@PathVariable Long id) {
        Optional<StudentProfile> profile = careerService.getStudentProfile(id);
        return profile.map(p -> ResponseEntity.ok(p))
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/profiles")
    public ResponseEntity<List<StudentProfile>> getAllProfiles() {
        List<StudentProfile> profiles = careerService.getAllStudentProfiles();
        return ResponseEntity.ok(profiles);
    }

    @PutMapping("/profile/{id}")
    public ResponseEntity<StudentProfile> updateStudentProfile(@PathVariable Long id,
                                                               @Valid @RequestBody StudentProfile profile) {
        Optional<StudentProfile> existingProfile = careerService.getStudentProfile(id);
        if (existingProfile.isPresent()) {
            profile.setId(id);
            StudentProfile updatedProfile = careerService.saveStudentProfile(profile);
            return ResponseEntity.ok(updatedProfile);
        }
        return ResponseEntity.notFound().build();
    }

    @DeleteMapping("/profile/{id}")
    public ResponseEntity<Void> deleteStudentProfile(@PathVariable Long id) {
        Optional<StudentProfile> profile = careerService.getStudentProfile(id);
        if (profile.isPresent()) {
            // In a real application, you would implement delete functionality
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    @PostMapping("/recommendations/{studentId}")
    public Mono<ResponseEntity<List<CareerRecommendation>>> generateRecommendations(@PathVariable Long studentId) {
        logger.info("Generating recommendations for student ID: {}", studentId);

        return careerService.generateCareerRecommendations(studentId)
                .map(recommendations -> {
                    if (recommendations.isEmpty()) {
                        return ResponseEntity.notFound().<List<CareerRecommendation>>build();
                    }
                    return ResponseEntity.ok(recommendations);
                })
                .onErrorReturn(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build());
    }

    @GetMapping("/recommendations/basic/{studentId}")
    public ResponseEntity<List<CareerRecommendation>> getBasicRecommendations(@PathVariable Long studentId) {
        Optional<StudentProfile> profileOpt = careerService.getStudentProfile(studentId);
        if (profileOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        List<CareerRecommendation> recommendations = careerService.getBasicRecommendations(profileOpt.get());
        return ResponseEntity.ok(recommendations);
    }

    @GetMapping("/streams")
    public ResponseEntity<List<IndianEducationStream>> getEducationStreams() {
        List<IndianEducationStream> streams = careerService.getEducationStreams();
        return ResponseEntity.ok(streams);
    }

    @GetMapping("/streams/level/{level}")
    public ResponseEntity<List<IndianEducationStream>> getStreamsByLevel(@PathVariable String level) {
        List<IndianEducationStream> streams = careerService.getStreamsByLevel(level);
        return ResponseEntity.ok(streams);
    }

    @GetMapping("/exams/{streamName}")
    public ResponseEntity<List<String>> getExamsForStream(@PathVariable String streamName) {
        List<String> exams = careerService.getCommonExamsForStream(streamName);
        return ResponseEntity.ok(exams);
    }

    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Career Guidance Engine is running!");
    }
}
