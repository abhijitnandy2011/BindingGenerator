#pragma once

#ifdef __BINDING_GENERATOR__
#define HIDDEN __attribute__((annotate("hidden")))
#define SCRIPTED __attribute__((annotate("scripted")))
#else
#define HIDDEN
#define SCRIPTED
#endif

SCRIPTED class TextComponent
{
public:
    TextComponent();

    std::string text() const;
    void setText(const std::string& value);

    HIDDEN void superSecretFunction();

private:
    std::string m_text;
};
