package com.study.hellospring.service;

import com.study.hellospring.domain.Content;
import com.study.hellospring.repository.ContentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ContentService {

    private final ContentRepository contentRepository;

    public void writeContent(Content content){
        contentRepository.save(content);
    }

    public void editContent(int id, String texts, String password){
        Content content = contentRepository.findById(id);
        if(!content.getPassword().equals(password)){
            return;
        }
        content.setTexts(texts);
        LocalDateTime now = LocalDateTime.now();
        String formattedDate = now.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        content.setUpdateDate(formattedDate);

        contentRepository.edit(id, content);
    }

    public void deleteContent(int id, String password){
        Content content = contentRepository.findById(id);
        if(!content.getPassword().equals(password)){
            return;
        }
        contentRepository.delete(id);
    }

    public List<Content> getAllContents(){
        return contentRepository.findAll();
    }

    public Content getContent(int id){
        return contentRepository.findById(id);
    }
}
