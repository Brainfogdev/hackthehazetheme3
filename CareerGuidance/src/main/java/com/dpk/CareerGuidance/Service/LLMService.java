package com.dpk.CareerGuidance.Service;

import com.dpk.CareerGuidance.Model.StudentProfile;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Map;

@Service
public class LLMService {
    private static final Logger logger = LoggerFactory.getLogger(LLMService.class);

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    @Value("${llm.api.key}")
    private String apiKey;

    @Value("${llm.api.model}")
    private String model;

    @Value("${llm.api.max-tokens}")
    private Integer maxTokens;

    public LLMService(WebClient.Builder webClientBuilder, ObjectMapper objectMapper) {
        this.webClient = webClientBuilder.baseUrl("https://api.openai.com/v1").build();
        this.objectMapper = objectMapper;
    }

    public Mono<String> generateCareerRecommendation(String prompt) {
        logger.debug("Generating career recommendation with prompt: {}", prompt);

        Map<String, Object> requestBody = Map.of(
                "model", model,
                "messages", new Object[]{
                        Map.of("role", "user", "content", prompt)
                },
                "max_tokens", maxTokens,
                "temperature", 0.7
        );

        return webClient.post()
                .uri("/chat/completions")
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(String.class)
                .map(this::extractContentFromResponse)
                .doOnSuccess(response -> logger.debug("LLM Response received: {}", response))
                .doOnError(error -> logger.error("Error calling LLM API: {}", error.getMessage()));
    }

    private String extractContentFromResponse(String response) {
        try {
            JsonNode jsonNode = objectMapper.readTree(response);
            return jsonNode.path("choices")
                    .get(0)
                    .path("message")
                    .path("content")
                    .asText();
        } catch (Exception e) {
            logger.error("Error parsing LLM response: {}", e.getMessage());
            return "Error processing recommendation. Please try again.";
        }
    }

    public String buildCareerGuidancePrompt(StudentProfile profile) {
        StringBuilder prompt = new StringBuilder();

        prompt.append("You are an expert career counselor specializing in the Indian education system. ");
        prompt.append("Analyze the following student profile and provide personalized career recommendations.\n\n");

        prompt.append("Student Profile:\n");
        prompt.append("- Name: ").append(profile.getName()).append("\n");
        prompt.append("- Age: ").append(profile.getAge()).append("\n");
        prompt.append("- Current Class: ").append(profile.getCurrentClass()).append("\n");
        prompt.append("- Current Stream: ").append(profile.getCurrentStream()).append("\n");
        prompt.append("- Subjects: ").append(String.join(", ", profile.getSubjects())).append("\n");
        prompt.append("- Interests: ").append(String.join(", ", profile.getInterests())).append("\n");
        prompt.append("- Skills: ").append(String.join(", ", profile.getSkills())).append("\n");
        prompt.append("- Career Aspirations: ").append(String.join(", ", profile.getCareerAspirations())).append("\n");
        prompt.append("- Academic Performance: ").append(profile.getAcademicPerformance()).append("\n");
        prompt.append("- Location: ").append(profile.getLocation()).append("\n");
        prompt.append("- Family Background: ").append(profile.getFamilyBackground()).append("\n");
        prompt.append("- Economic Status: ").append(profile.getEconomicStatus()).append("\n");

        if (profile.getExamScores() != null && !profile.getExamScores().isEmpty()) {
            prompt.append("- Exam Scores: ");
            profile.getExamScores().forEach((exam, score) ->
                    prompt.append(exam).append(": ").append(score).append("%, "));
            prompt.append("\n");
        }

        prompt.append("\nPlease provide a comprehensive career recommendation in JSON format with the following structure:\n");
        prompt.append("{\n");
        prompt.append("  \"recommendations\": [\n");
        prompt.append("    {\n");
        prompt.append("      \"careerPath\": \"Career name\",\n");
        prompt.append("      \"description\": \"Brief description\",\n");
        prompt.append("      \"matchPercentage\": 85,\n");
        prompt.append("      \"requiredSkills\": [\"skill1\", \"skill2\"],\n");
        prompt.append("      \"recommendedExams\": [\"JEE\", \"NEET\"],\n");
        prompt.append("      \"suggestedCourses\": [\"B.Tech\", \"B.Sc\"],\n");
        prompt.append("      \"topColleges\": [\"IIT Delhi\", \"IISc\"],\n");
        prompt.append("      \"expectedSalaryRange\": \"5-15 LPA\",\n");
        prompt.append("      \"jobMarketTrend\": \"Growing\",\n");
        prompt.append("      \"alternativeCareers\": [\"alt1\", \"alt2\"],\n");
        prompt.append("      \"roadmap\": \"Step-by-step career roadmap\",\n");
        prompt.append("      \"skillGaps\": [\"gap1\", \"gap2\"],\n");
        prompt.append("      \"reasoning\": \"Why this career matches the profile\"\n");
        prompt.append("    }\n");
        prompt.append("  ]\n");
        prompt.append("}\n\n");

        prompt.append("Consider Indian education streams, entrance exams (JEE, NEET, CLAT, CAT, GATE, etc.), ");
        prompt.append("job market trends in India, salary expectations, and regional opportunities. ");
        prompt.append("Provide 3-5 career recommendations ranked by match percentage.");

        return prompt.toString();
    }
}
