package com.dpk.CareerGuidance.Service;

import com.dpk.CareerGuidance.Model.CareerRecommendation;
import com.dpk.CareerGuidance.Model.IndianEducationStream;
import com.dpk.CareerGuidance.Model.StudentProfile;
import com.dpk.CareerGuidance.Repository.StudentProfileRepository;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class CareerGuidanceService {
    private static final Logger logger = LoggerFactory.getLogger(CareerGuidanceService.class);

    private final StudentProfileRepository studentRepository;
    private final LLMService llmService;
    private final ObjectMapper objectMapper;
    private final List<IndianEducationStream> educationStreams;
    private final Map<String, Object> careerPathsData;

    public CareerGuidanceService(StudentProfileRepository studentRepository,
                                 LLMService llmService,
                                 ObjectMapper objectMapper) {
        this.studentRepository = studentRepository;
        this.llmService = llmService;
        this.objectMapper = objectMapper;
        this.educationStreams = loadEducationStreams();
        this.careerPathsData = loadCareerPathsData();
    }

    public StudentProfile saveStudentProfile(StudentProfile profile) {
        logger.info("Saving student profile for: {}", profile.getName());
        return studentRepository.save(profile);
    }

    public Optional<StudentProfile> getStudentProfile(Long id) {
        return studentRepository.findById(id);
    }

    public List<StudentProfile> getAllStudentProfiles() {
        return studentRepository.findAll();
    }

    public Mono<List<CareerRecommendation>> generateCareerRecommendations(Long studentId) {
        logger.info("Generating career recommendations for student ID: {}", studentId);

        Optional<StudentProfile> profileOpt = studentRepository.findById(studentId);
        if (profileOpt.isEmpty()) {
            return Mono.just(Collections.emptyList());
        }

        StudentProfile profile = profileOpt.get();
        String prompt = llmService.buildCareerGuidancePrompt(profile);

        return llmService.generateCareerRecommendation(prompt)
                .map(this::parseRecommendationsFromLLMResponse)
                .doOnSuccess(recommendations ->
                        logger.info("Generated {} recommendations for student: {}",
                                recommendations.size(), profile.getName()))
                .onErrorReturn(this.getFallbackRecommendations(profile));
    }

    public List<IndianEducationStream> getEducationStreams() {
        return educationStreams;
    }

    public List<IndianEducationStream> getStreamsByLevel(String level) {
        return educationStreams.stream()
                .filter(stream -> stream.getLevel().equalsIgnoreCase(level))
                .collect(Collectors.toList());
    }

    public List<String> getCommonExamsForStream(String streamName) {
        return educationStreams.stream()
                .filter(stream -> stream.getStreamName().equalsIgnoreCase(streamName))
                .findFirst()
                .map(IndianEducationStream::getCommonExams)
                .orElse(Collections.emptyList());
    }

    public List<CareerRecommendation> getBasicRecommendations(StudentProfile profile) {
        // Fallback recommendations based on basic matching
        List<CareerRecommendation> recommendations = new ArrayList<>();

        // Simple rule-based recommendations
        if (profile.getCurrentStream().toLowerCase().contains("science")) {
            if (profile.getInterests().stream().anyMatch(i -> i.toLowerCase().contains("medicine"))) {
                recommendations.add(createBasicRecommendation("Medical Doctor",
                        "Healthcare professional treating patients", 85.0));
            }
            if (profile.getInterests().stream().anyMatch(i -> i.toLowerCase().contains("engineering"))) {
                recommendations.add(createBasicRecommendation("Software Engineer",
                        "Develop software applications and systems", 80.0));
            }
        }

        if (profile.getCurrentStream().toLowerCase().contains("commerce")) {
            recommendations.add(createBasicRecommendation("Chartered Accountant",
                    "Financial expert and auditor", 85.0));
            recommendations.add(createBasicRecommendation("Investment Banking",
                    "Financial services and investment advisory", 75.0));
        }

        if (profile.getCurrentStream().toLowerCase().contains("arts")) {
            recommendations.add(createBasicRecommendation("Civil Services",
                    "Government administrative services", 80.0));
            recommendations.add(createBasicRecommendation("Journalism",
                    "Media and communication professional", 70.0));
        }

        return recommendations;
    }

    private CareerRecommendation createBasicRecommendation(String careerPath, String description, double matchPercentage) {
        CareerRecommendation recommendation = new CareerRecommendation(careerPath, description, matchPercentage);

        // Set some default values based on career
        switch (careerPath.toLowerCase()) {
            case "medical doctor":
                recommendation.setRecommendedExams(Arrays.asList("NEET", "AIIMS"));
                recommendation.setSuggestedCourses(Arrays.asList("B.Com", "BBA"));
                recommendation.setTopColleges(Arrays.asList("SRCC Delhi", "LSR Delhi", "Christ University"));
                recommendation.setExpectedSalaryRange("5-20 LPA");
                break;
        }

        recommendation.setJobMarketTrend("Growing");
        recommendation.setReasoning("Based on current stream and basic profile matching");

        return recommendation;
    }

    private List<CareerRecommendation> parseRecommendationsFromLLMResponse(String llmResponse) {
        try {
            // Try to extract JSON from the response
            String jsonPart = extractJsonFromResponse(llmResponse);
            JsonNode jsonNode = objectMapper.readTree(jsonPart);
            JsonNode recommendations = jsonNode.path("recommendations");

            List<CareerRecommendation> result = new ArrayList<>();

            if (recommendations.isArray()) {
                for (JsonNode recNode : recommendations) {
                    CareerRecommendation rec = new CareerRecommendation();
                    rec.setCareerPath(recNode.path("careerPath").asText());
                    rec.setDescription(recNode.path("description").asText());
                    rec.setMatchPercentage(recNode.path("matchPercentage").asDouble());
                    rec.setRequiredSkills(extractStringList(recNode.path("requiredSkills")));
                    rec.setRecommendedExams(extractStringList(recNode.path("recommendedExams")));
                    rec.setSuggestedCourses(extractStringList(recNode.path("suggestedCourses")));
                    rec.setTopColleges(extractStringList(recNode.path("topColleges")));
                    rec.setExpectedSalaryRange(recNode.path("expectedSalaryRange").asText());
                    rec.setJobMarketTrend(recNode.path("jobMarketTrend").asText());
                    rec.setAlternativeCareers(extractStringList(recNode.path("alternativeCareers")));
                    rec.setRoadmap(recNode.path("roadmap").asText());
                    rec.setSkillGaps(extractStringList(recNode.path("skillGaps")));
                    rec.setReasoning(recNode.path("reasoning").asText());

                    result.add(rec);
                }
            }

            return result;
        } catch (Exception e) {
            logger.error("Error parsing LLM response: {}", e.getMessage());
            return Collections.emptyList();
        }
    }

    private String extractJsonFromResponse(String response) {
        // Find JSON content between { and }
        int startIndex = response.indexOf('{');
        int endIndex = response.lastIndexOf('}');

        if (startIndex != -1 && endIndex != -1 && endIndex > startIndex) {
            return response.substring(startIndex, endIndex + 1);
        }

        return response;
    }

    private List<String> extractStringList(JsonNode arrayNode) {
        List<String> result = new ArrayList<>();
        if (arrayNode.isArray()) {
            for (JsonNode item : arrayNode) {
                result.add(item.asText());
            }
        }
        return result;
    }

    private List<CareerRecommendation> getFallbackRecommendations(StudentProfile profile) {
        logger.warn("Using fallback recommendations for profile: {}", profile.getName());
        return getBasicRecommendations(profile);
    }

    private List<IndianEducationStream> loadEducationStreams() {
        try {
            ClassPathResource resource = new ClassPathResource("data/indian-streams.json");
            return objectMapper.readValue(resource.getInputStream(),
                    new TypeReference<List<IndianEducationStream>>() {});
        } catch (IOException e) {
            logger.error("Error loading education streams data: {}", e.getMessage());
            return getDefaultEducationStreams();
        }
    }

    private Map<String, Object> loadCareerPathsData() {
        try {
            ClassPathResource resource = new ClassPathResource("data/career-paths.json");
            return objectMapper.readValue(resource.getInputStream(),
                    new TypeReference<Map<String, Object>>() {});
        } catch (IOException e) {
            logger.error("Error loading career paths data: {}", e.getMessage());
            return new HashMap<>();
        }
    }

    private List<IndianEducationStream> getDefaultEducationStreams() {
        List<IndianEducationStream> streams = new ArrayList<>();

        // Science Stream
        IndianEducationStream science = new IndianEducationStream("Science", "12th");
        science.setSubjects(Arrays.asList("Physics", "Chemistry", "Mathematics", "Biology"));
        science.setCommonExams(Arrays.asList("JEE Main", "JEE Advanced", "NEET", "BITSAT"));
        science.setCareerOptions(Arrays.asList("Engineering", "Medical", "Research", "Technology"));
        science.setTopColleges(Arrays.asList("IIT Delhi", "IIT Bombay", "AIIMS", "BITS Pilani"));
        streams.add(science);

        // Commerce Stream
        IndianEducationStream commerce = new IndianEducationStream("Commerce", "12th");
        commerce.setSubjects(Arrays.asList("Accountancy", "Business Studies", "Economics", "Mathematics"));
        commerce.setCommonExams(Arrays.asList("CA Foundation", "CS Foundation", "CMA Foundation", "CLAT"));
        commerce.setCareerOptions(Arrays.asList("Chartered Accountancy", "Banking", "Finance", "Business"));
        commerce.setTopColleges(Arrays.asList("SRCC Delhi", "LSR Delhi", "Christ University"));
        streams.add(commerce);

        // Arts Stream
        IndianEducationStream arts = new IndianEducationStream("Arts", "12th");
        arts.setSubjects(Arrays.asList("History", "Political Science", "Geography", "Literature"));
        arts.setCommonExams(Arrays.asList("CLAT", "UPSC", "State PSC", "JNU Entrance"));
        arts.setCareerOptions(Arrays.asList("Civil Services", "Law", "Journalism", "Teaching"));
        arts.setTopColleges(Arrays.asList("JNU Delhi", "BHU Varanasi", "Jadavpur University"));
        streams.add(arts);

        return streams;
    }
}
