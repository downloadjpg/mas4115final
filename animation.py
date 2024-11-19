from manim import *
import numpy as np

'''
TODO:
- [ ] Track and bounds
- [ ] Cart wheels?
- [ ] Make something happen on failure state... stop animation?

'''
class InvertedPendulumAnimation(Scene):
    time = 0.0
    def construct(self):
        VISUAL_FACTOR = 4
        # Constants
        cart_width = 0.2 * VISUAL_FACTOR
        cart_height = 0.1 * VISUAL_FACTOR
        pendulum_length = 0.5 * VISUAL_FACTOR 
        circle_radius = 0.06 * VISUAL_FACTOR


        # load simulation data
        h = np.load("data/h_values.npy") * VISUAL_FACTOR# Cart positions
        theta = np.load("data/theta_values.npy")
        time_step = 0.02

        # Cart
        cart = Rectangle(width=cart_width, height=cart_height, color=BLUE)
        cart.move_to(ORIGIN) # Start cart at origin

        # Pendulum
        pendulum_line = Line(ORIGIN, ORIGIN + pendulum_length * UP, color=YELLOW)
        pendulum_mass = Dot(ORIGIN + pendulum_length * UP, radius=circle_radius, color=RED)

        #Group pendulum together?
        pendulum = VGroup(pendulum_line, pendulum_mass)
        system = VGroup(cart, pendulum)

        self.add(cart, pendulum)

         # Animation function
        def update_system(mob, dt):
            # Get the current time index
            time_idx = int(self.time / time_step) % len(h)
            cart.move_to([h[time_idx], 0, 0])  # Update cart position
            pendulum_line.put_start_and_end_on(
                [h[time_idx], 0, 0],  # Start at the cart's center
                [   
                    h[time_idx] + pendulum_length * np.sin(theta[time_idx]), 
                    pendulum_length * np.cos(theta[time_idx]), 
                    0
                ]
            )
            pendulum_mass.move_to(pendulum_line.get_end())  # Attach to the line's end
            self.time += dt

        # Continuously update
        system.add_updater(update_system)

        # Play animation
        self.play(FadeIn(system))
        self.wait(len(h) * time_step)

        # End scene
        self.play(FadeOut(cart), FadeOut(pendulum))