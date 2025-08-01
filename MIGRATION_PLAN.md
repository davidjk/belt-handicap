# JAR System Migration: Streamlit → Vanilla JS + Modern Visual Design

## Overview
Migrate the JAR (Jiu-Jitsu Attribute Rating) System from Streamlit to a vanilla JavaScript frontend with a visually striking, modern interface that makes BJJ scoring feel engaging and dynamic.

## Visual Design Goals - "Make it Look Cool"

### UI/UX Inspiration
- **Gaming aesthetics** - Think Puzzle Fighter character select screens with practitioner avatars/cards
- **Sports analytics dashboards** - NBA/NFL stat visualizations with smooth animations
- **Modern web apps** - Sleek gradients, subtle shadows, smooth micro-interactions
- **Data visualization** - Animated charts that respond to input changes in real-time

### Specific Visual Elements to Explore
- **Practitioner Cards** - Avatar/silhouette representations of fighters with belt colors
- **Animated Radar Charts** - Smooth transitions when factors change, pulsing effects for significant factors
- **Real-time Visual Feedback** - Input changes trigger immediate visual responses (color shifts, animations)
- **Factor Impact Indicators** - Visual bars or meters showing how each factor affects the score
- **Cinematic Transitions** - Smooth page sections, staggered animations for results
- **BJJ Theming** - Subtle martial arts imagery, belt color schemes, mat textures
- **Interactive Elements** - Hover states, button animations, form field focus effects

### Technical Implementation Ideas
- **CSS Animations** - Keyframes for smooth transitions and micro-interactions
- **Custom Properties** - Easy theme switching (light/dark, different gyms)
- **Chart.js Animations** - Smooth radar chart updates with custom easing
- **Intersection Observer** - Scroll-triggered animations for sections
- **CSS Grid/Flexbox** - Modern layouts with responsive design
- **Gradient Backgrounds** - Dynamic color schemes that respond to calculations

## Technical Approach

### Tech Stack Decision
- **Vanilla JavaScript** (no React/Vue/Angular)
- **Vite** for development tooling and build process
- **GitHub Pages** for static hosting
- **Chart.js** for animated radar chart visualization
- **CSS Custom Properties** for design system flexibility

### Architecture Changes
- Single-page calculator application
- Real-time score calculation with visual feedback
- No practitioner storage (simplifies state management)
- Client-side only - all logic runs in browser

### Design System Architecture
- **Semantic CSS** with component-based classes
- **Design tokens** for consistent spacing, colors, typography
- **Animation system** for cohesive micro-interactions
- **Responsive design** that works on mobile and desktop
- **Accessibility-first** approach with ARIA labels and keyboard navigation

### Migration Tasks
- [ ] Convert Python calculation logic to JavaScript
- [ ] Design visual mockups/wireframes for "cool" interface
- [ ] Build semantic HTML structure with accessibility
- [ ] Create CSS design system with custom properties and animations
- [ ] Implement real-time form updates with visual feedback
- [ ] Add animated radar chart visualization
- [ ] Explore practitioner avatar/card representations
- [ ] Add micro-interactions and hover states
- [ ] Set up Vite build process
- [ ] Deploy to GitHub Pages

## Success Criteria
- Users think "this looks professional and engaging"
- Real-time visual feedback makes the calculator feel responsive
- Visual design enhances understanding of the JAR system factors
- Interface feels modern compared to typical web calculators
- Maintains full accessibility and usability

## References
- Current Streamlit app architecture documented in CLAUDE.md
- JAR System specification in docs/initial_prd.md