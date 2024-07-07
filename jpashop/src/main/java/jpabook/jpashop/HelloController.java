package jpabook.jpashop;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HelloController {
    @GetMapping("hello")
    public String hello(Model model){ //컨트롤러에서 뷰로 데이터를 넘길 수 있음
        model.addAttribute("data", "hello!!"); //넘길 데이터
        return "hello"; //화면 이름, .html 자동으로 붙음
    }
}
