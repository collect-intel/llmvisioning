import streamlit as st
import anthropic

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

@st.cache_data(show_spinner=False)
def generate_options(prompt, n=3):
    response = client.completions.create(
        model="claude-2.1",
        prompt=f"\n\nHuman: {prompt}\n\nPlease provide {n} distinct options (split by '\n\n' i.e. TWO newlines, but without numbering the options):\n\nAssistant: Certainly! Here are {n} distinct options based on your request:\n\n",
        max_tokens_to_sample=300 * n,
        temperature=0.7
    )
    options = response.completion.split("\n\n")
    return [option.strip() for option in options if option.strip()]

def main():
    st.title("Future Technology Scenario Explorer")

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 0

    # Page navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous") and st.session_state.page > 0:
            st.session_state.page -= 1
    with col2:
        if st.button("Next") and st.session_state.page < 11:
            st.session_state.page += 1

    # Page content
    if st.session_state.page == 0:
        st.subheader("Step 1: Describe Your Scenario")
        st.session_state.scenario_description = st.text_input("Describe the type of scenario you're interested in exploring (1 sentence):", st.session_state.get('scenario_description', ''))

    elif st.session_state.page == 1:
        st.subheader("Step 2: Select a Scenario")
        if 'scenarios' not in st.session_state:
            with st.spinner("Generating scenarios..."):
                st.session_state.scenarios = generate_options(f"Generate 3 detailed and diverse scenarios based on this description: {st.session_state.scenario_description}", n=3)
        
        st.write("Select a scenario to explore:")
        scenarios = [f"Scenario {i+1}: {scenario}" for i, scenario in enumerate(st.session_state.scenarios)]
        selected_scenario = st.radio("", scenarios, key="scenario_selection")
    
        # Extract the selected scenario text
        if selected_scenario:
            scenario_index = int(selected_scenario.split(":")[0].split()[-1]) - 1
            st.session_state.selected_scenario = st.session_state.scenarios[scenario_index]

    elif st.session_state.page == 2:
        st.subheader("Step 3: Identify Areas of Impact")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")

        st.write("If this scenario happened, what areas of life do you think will be changed/impacted?")
        user_impacts = []
        for i in range(3):
            impact = st.text_input(f"Impact {i+1}", key=f"user_impact_{i}")
            if impact:
                user_impacts.append(impact)
        
        # Generate AI drivers
        if 'ai_impacts' not in st.session_state:
            with st.spinner("Generating additional impacts..."):
                st.session_state.ai_impacts = generate_options(f"Generate 10 potential areas of life that could change, if this scenario happened: {st.session_state.selected_scenario}", n=10)

        # Display all drivers and allow selection
        st.write("Select plausible impacts:")
        all_impacts = user_impacts + st.session_state.ai_impacts
        selected_impacts = []
        for i, impact in enumerate(all_impacts):
            if st.checkbox(impact, key=f"impact_{i}"):
                selected_impacts.append(impact)
        
        st.session_state.selected_impacts = selected_impacts
        st.write("Selected impacts:", ", ".join(st.session_state.selected_impacts))

    elif st.session_state.page == 3:
        st.subheader("Step 4: Identify Best Aspects")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
        
        st.write("What do you think are the best aspects of this scenario?")
        user_best_aspects = []
        for i in range(3):
            best_aspect = st.text_input(f"Best aspect {i+1}", key=f"user_best_aspect_{i}")
            if best_aspect:
                user_best_aspects.append(best_aspect)
        
        if 'ai_best_aspects' not in st.session_state:
            with st.spinner("Generating additional aspects..."):
                st.session_state.ai_best_aspects = generate_options(f"Generate 10 potential aspects of the following scenario that are likely to be the best aspects of it: {st.session_state.selected_scenario}", n=10)

        # Display all aspects and allow selection
        st.write("Select plausible best aspects:")
        all_best_aspects = user_best_aspects + st.session_state.ai_best_aspects
        selected_best_aspects = []
        for i, best_aspect in enumerate(all_best_aspects):
            if st.checkbox(best_aspect, key=f"best_aspect_{i}"):
                selected_best_aspects.append(best_aspect)
        
        st.session_state.selected_best_aspects = selected_best_aspects
        st.write("Selected best aspects:", ", ".join(st.session_state.selected_best_aspects))

    elif st.session_state.page == 4:
        st.subheader("Step 5: Identify Worst Aspects")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
    
        st.write("What do you think are the worst aspects of this scenario?")
        user_worst_aspects = []
        for i in range(3):
            worst_aspect = st.text_input(f"Worst aspect {i+1}", key=f"user_worst_aspect_{i}")
            if worst_aspect:
                user_worst_aspects.append(best_aspect)
        
        if 'ai_worst_aspects' not in st.session_state:
            with st.spinner("Generating additional aspects..."):
                st.session_state.ai_worst_aspects = generate_options(f"Generate 10 potential aspects of the following scenario that are likely to be the worst aspects of it: {st.session_state.selected_scenario}", n=10)

        # Display all aspects and allow selection
        st.write("Select plausible worst aspects:")
        all_worst_aspects = user_worst_aspects + st.session_state.ai_worst_aspects
        selected_worst_aspects = []
        for i, worst_aspect in enumerate(all_worst_aspects):
            if st.checkbox(worst_aspect, key=f"worst_aspect_{i}"):
                selected_worst_aspects.append(worst_aspect)
        
        st.session_state.selected_worst_aspects = selected_worst_aspects
        st.write("Selected worst aspects:", ", ".join(st.session_state.selected_worst_aspects))

    elif st.session_state.page == 5:
        st.subheader("Step 4: Identify Drivers")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
        
        # User input for drivers
        st.write("What kinds of 'drivers' or driving forces are likely to encourage this scenario to happen?")
        user_drivers = []
        for i in range(3):
            driver = st.text_input(f"Driver {i+1}", key=f"user_driver_{i}")
            if driver:
                user_drivers.append(driver)
        
        # Generate AI drivers
        if 'ai_drivers' not in st.session_state:
            with st.spinner("Generating additional drivers..."):
                st.session_state.ai_drivers = generate_options(f"Generate 10 potential societal drivers / driving forces for this scenario that are likely to encourage it to happen: {st.session_state.selected_scenario}", n=10)

        # Display all drivers and allow selection
        st.write("Select plausible drivers:")
        all_drivers = user_drivers + st.session_state.ai_drivers
        selected_drivers = []
        for i, driver in enumerate(all_drivers):
            if st.checkbox(driver, key=f"driver_{i}"):
                selected_drivers.append(driver)
        
        st.session_state.selected_drivers = selected_drivers
        st.write("Selected drivers:", ", ".join(st.session_state.selected_drivers))

    elif st.session_state.page == 6:
        st.subheader("Step 5: Identify Barriers and Inhibitors")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
        
        # User input for barriers
        st.write("What barriers / inhibitors are likely to prevent this scenario from happening?")
        user_barriers = []
        for i in range(3):
            barrier = st.text_input(f"Barrier {i+1}", key=f"user_barrier_{i}")
            if barrier:
                user_barriers.append(barrier)
        
        # Generate AI barriers
        if 'ai_barriers' not in st.session_state:
            with st.spinner("Generating additional barriers..."):
                st.session_state.ai_barriers = generate_options(f"Generate 10 potential societal barriers or inhibitors for this scenario that are likely to prevent it from happening: {st.session_state.selected_scenario}", n=10)

        # Display all barriers and allow selection
        st.write("Select relevant barriers:")
        all_barriers = user_barriers + st.session_state.ai_barriers
        selected_barriers = []
        for i, barrier in enumerate(all_barriers):
            if st.checkbox(barrier, key=f"barrier_{i}"):
                selected_barriers.append(barrier)
        
        st.session_state.selected_barriers = selected_barriers
        st.write("Selected barriers:", ", ".join(st.session_state.selected_barriers))

    elif st.session_state.page == 7:
        st.subheader("Step 7: Strategies to Mitigate the Worst Parts")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
        st.write("How do you think that as a society, we could mitigate the worst parts of this scenario?")
        
        # User input for mitigation strategies
        st.write("Enter your own mitigation strategies:")
        user_mitigations = []
        for i in range(3):
            mitigation = st.text_input(f"Mitigation Strategy {i+1}", key=f"user_mitigation_{i}")
            if mitigation:
                user_mitigations.append(mitigation)
        
        # Generate AI mitigation strategies
        if 'ai_mitigations' not in st.session_state:
            with st.spinner("Generating additional mitigation strategies..."):
                st.session_state.ai_mitigations = generate_options(f"Generate 10 ways that society/various actors could mitigate the negative aspects of this scenario: {st.session_state.selected_scenario}", n=10)

        # Display all mitigation strategies and allow selection
        st.write("Select relevant mitigation strategies:")
        all_mitigations = user_mitigations + st.session_state.ai_mitigations
        selected_mitigations = []
        for i, mitigation in enumerate(all_mitigations):
            if st.checkbox(mitigation, key=f"mitigation_{i}"):
                selected_mitigations.append(mitigation)
        
        st.session_state.selected_mitigations = selected_mitigations
        st.write("Selected mitigation strategies:", ", ".join(st.session_state.selected_mitigations))

    elif st.session_state.page == 8:
        st.subheader("Step 8: Strategies to Enable / Accentuate the Best Parts")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
        st.write("How do you think that as a society, we could enable / accentuate the best parts of this scenario?")
        
        # User input for accentuation strategies
        st.write("Enter your own accentuation strategies:")
        user_accentuations = []
        for i in range(3):
            accentuation = st.text_input(f"Accentuation Strategy {i+1}", key=f"user_accentuation_{i}")
            if accentuation:
                user_accentuations.append(accentuation)
        
        # Generate AI accentuation strategies
        if 'ai_accentuations' not in st.session_state:
            with st.spinner("Generating additional accentuation strategies..."):
                st.session_state.ai_accentuations = generate_options(f"Generate 10 ways that society/various actors could bring out the positive aspects of this scenario: {st.session_state.selected_scenario}", n=10)

        # Display all accentuation strategies and allow selection
        st.write("Select relevant accentuation strategies:")
        all_accentuations = user_accentuations + st.session_state.ai_accentuations
        selected_accentuations = []
        for i, accentuation in enumerate(all_accentuations):
            if st.checkbox(accentuation, key=f"accentuation_{i}"):
                selected_accentuations.append(accentuation)
        
        st.session_state.selected_accentuations = selected_accentuations
        st.write("Selected accentuation strategies:", ", ".join(st.session_state.selected_accentuations))

    elif st.session_state.page == 9:
        st.subheader("Step 3: Evaluate the Scenario")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
        st.session_state.likelihood = st.slider("Rate the likelihood of this scenario: (from 1-10, 10 being most likely)", 1, 10, 5)
        st.session_state.desirability = st.slider("Rate the desirability of this scenario (from 1-10, 10 being most desirable):", 1, 10, 5)

    elif st.session_state.page == 10:
        st.subheader("Step 9: Backcasting")
        st.write(f"Selected scenario: {st.session_state.selected_scenario}")
        st.write("This is your last question before we summarize your scenario exploration. Given this exploration, what do you think we can do _now_ to make sure this scenario does/doesn't happen, or to make sure it happens well?")
        # User input for paths
        st.write("Enter your own pathways:")
        user_backcast_paths = []
        for i in range(2):
            path = st.text_input(f"Pathway {i+1}", key=f"user_backcast_{i}")
            if path:
                user_backcast_paths.append(path)
        
        # Generate AI backcast paths
        if 'ai_backcast_paths' not in st.session_state:
            with st.spinner("Generating additional pathways..."):
                st.session_state.ai_backcast_paths = generate_options(f"Generate 5 plausible pathways to reach the positive aspects and avoid the negative aspects of this scenario: {st.session_state.selected_scenario}", n=5)

        # Display all backcast paths and allow selection
        st.write("Select a plausible pathway:")
        all_paths = user_backcast_paths + st.session_state.ai_backcast_paths
        selected_paths = []
        for i, path in enumerate(all_paths):
            if st.radio(f"Pathway {i+1}", [path], key=f"backcast_{i}"):
                selected_paths.append(path)
 
        st.session_state.selected_paths = selected_paths
        st.write("Selected paths:", ", ".join(st.session_state.selected_paths))

    elif st.session_state.page == 11:
        st.subheader("Summary")
        # create a generated summary
        response = client.completions.create(
            model="claude-2.1",
            prompt=f"""\n\nHuman: Here is a summary of a technological future scenario that I have just explored.
This describes the scenario: {st.session_state.selected_scenario}

I rated the scenario's likelihood {st.session_state.likelihood}/10 and desirabilty {st.session_state.desirability}/10. 
I thought the biggest areas of life this would impact were {', '.join(st.session_state.selected_impacts)}.
I thought the main positive aspects were {', '.join(st.session_state.selected_best_aspects)} and the main negative aspects were {', '.join(st.session_state.selected_worst_aspects)}.
I thought the main drivers that might enable this scenario to happen were {', '.join(st.session_state.selected_drivers)} and the main barriers were {', '.join(st.session_state.selected_barriers)}.
I brainstormed some strategies to: 
1. Mitigate the bad parts, which were: {', '.join(st.session_state.selected_mitigations)}
2. Enable the good parts: {', '.join(st.session_state.selected_accentuations)}
Finally, I thought that even today, we could do these things to ensure the best future, given the details of this scenario: {st.session_state.selected_paths}

Please thoughtfully and accurately summarize my views on this scenario and give me some takeaways to think about / reflection on. (Do NOT output any additional comments as a preamble or after you write. For example, I do not want you to say 'Please let me know if you'd like me to expand on any of this' or the like.)\n\nAssistant:""",
            max_tokens_to_sample=1000,
            temperature=0.7
        )

        summary = f"""
        AI-generated summary:
        {response.completion}

        Scenario: {st.session_state.selected_scenario}
        Likelihood: {st.session_state.likelihood}/10
        Desirability: {st.session_state.desirability}/10
         
        Selected Impacts:
        {', '.join(st.session_state.selected_impacts)}
        
        Selected Positive Aspects:
        {', '.join(st.session_state.selected_best_aspects)}
        
        Selected Negative Aspects:
        {', '.join(st.session_state.selected_worst_aspects)}
        
        Selected Drivers:
        {', '.join(st.session_state.selected_drivers)}
        
        Selected Barriers:
        {', '.join(st.session_state.selected_barriers)}
       
        Selected Mitigation Strategies:
        {', '.join(st.session_state.selected_mitigations)}
        
        Selected Accentuation Strategies:
        {', '.join(st.session_state.selected_accentuations)}
        
        Selected Beneficial Pathways:
        {st.session_state.selected_paths}
       """
        
        st.text_area("Summary", summary, height=400)

if __name__ == "__main__":
    main()