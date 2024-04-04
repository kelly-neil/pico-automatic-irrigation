function Section(title, desc, t_content) {
    return {
        title: title,
        desc: desc,
        t_content: t_content,
        $template: "#t_section"
    }
}

PetiteVue.createApp({
    
}).mount('#app')