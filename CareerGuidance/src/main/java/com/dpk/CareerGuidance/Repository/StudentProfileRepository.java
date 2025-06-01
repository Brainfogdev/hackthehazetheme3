package com.dpk.CareerGuidance.Repository;

import com.dpk.CareerGuidance.Model.StudentProfile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StudentProfileRepository extends JpaRepository<StudentProfile,Long> {
    List<StudentProfile> findByCurrentStream(String currentStream);

    List<StudentProfile> findByCurrentClass(String currentClass);

    List<StudentProfile> findByLocation(String location);

    @Query("SELECT sp FROM StudentProfile sp WHERE sp.age BETWEEN :minAge AND :maxAge")
    List<StudentProfile> findByAgeRange(@Param("minAge") Integer minAge, @Param("maxAge") Integer maxAge);

    @Query("SELECT sp FROM StudentProfile sp JOIN sp.interests i WHERE i IN :interests")
    List<StudentProfile> findByInterestsIn(@Param("interests") List<String> interests);

    @Query("SELECT sp FROM StudentProfile sp JOIN sp.skills s WHERE s IN :skills")
    List<StudentProfile> findBySkillsIn(@Param("skills") List<String> skills);

}
