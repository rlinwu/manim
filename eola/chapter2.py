from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import VMobject

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from mobject.vectorized_mobject import *

from eola.matrix import *
from eola.two_d_space import *

class OpeningQuote(Scene):
    def construct(self):
        words = TextMobject("""
            Mathematics requires a small dose, not of genius, \\\\
            but of an imaginative freedom which, in a larger \\\\
            dose, would be insanity.
        """)
        words.to_edge(UP)    
        for mob in words.submobjects[49:49+18]:
            mob.highlight(GREEN)
        author = TextMobject("-Angus K. Rodgers")
        author.highlight(YELLOW)
        author.next_to(words, DOWN, buff = 0.5)

        self.play(FadeIn(words))
        self.dither(3)
        self.play(Write(author, run_time = 3))
        self.dither()


class CoordinatesWereFamiliar(TeacherStudentsScene):
    def construct(self):
        self.setup()
        self.student_says("I know this already")
        self.random_blink()
        self.teacher_says("Ah, but there is a subtlety")
        self.random_blink()
        self.dither()


class CoordinatesAsScalars(VectorScene):
    CONFIG = {
        "vector_coords" : [3, -2]
    }

    def construct(self):
        self.axes = self.add_axes()
        vector = self.add_vector(self.vector_coords)
        array, x_line, y_line = self.vector_to_coords(vector)
        self.add(array)
        self.dither()
        new_array = self.general_idea_of_scalars(array, vector)
        self.scale_basis_vectors(new_array)
        self.show_symbolic_sum(new_array, vector)

    def general_idea_of_scalars(self, array, vector):
        starting_mobjects = self.get_mobjects()

        title = TextMobject("Think of each coordinate as a scalar")
        title.to_edge(UP)

        x, y = array.get_mob_matrix().flatten()
        new_x = x.copy().scale(2).highlight(X_COLOR)
        new_x.move_to(3*LEFT+2*UP)
        new_y = y.copy().scale(2).highlight(Y_COLOR)
        new_y.move_to(3*RIGHT+2*UP)

        i_hat, j_hat = self.get_basis_vectors()
        new_i_hat = Vector(
            self.vector_coords[0]*i_hat.get_end(), 
            color = X_COLOR
        )
        new_j_hat = Vector(
            self.vector_coords[1]*j_hat.get_end(), 
            color = Y_COLOR
        )
        VMobject(i_hat, new_i_hat).shift(3*LEFT)
        VMobject(j_hat, new_j_hat).shift(3*RIGHT)

        new_array = Matrix([new_x.copy(), new_y.copy()])
        new_array.scale(0.5)
        new_array.shift(
            -new_array.get_boundary_point(-vector.get_end()) + \
            1.1*vector.get_end()
        )

        self.remove(*starting_mobjects)
        self.play(
            Transform(x, new_x),
            Transform(y, new_y),
            Write(title),
        )
        self.play(FadeIn(i_hat), FadeIn(j_hat))
        self.dither()
        self.play(
            Transform(i_hat, new_i_hat),
            Transform(j_hat, new_j_hat),
            run_time = 3
        )
        self.dither()
        starting_mobjects.remove(array)

        new_x, new_y = new_array.get_mob_matrix().flatten()
        self.play(
            Transform(x, new_x),
            Transform(y, new_y),
            FadeOut(i_hat),
            FadeOut(j_hat),
            Write(new_array.get_brackets()),
            FadeIn(VMobject(*starting_mobjects)),
            FadeOut(title)
        )
        self.remove(x, y)
        self.add(new_array)
        return new_array

    def scale_basis_vectors(self, new_array):
        self.play(ApplyMethod(self.axes.highlight, GREY))
        i_hat, j_hat = self.get_basis_vectors()
        self.add_vector(i_hat)
        i_hat_label = self.label_vector(
            i_hat, "\\hat{\\imath}", 
            color = X_COLOR, 
            label_scale_val = 1
        )
        self.add_vector(j_hat)
        j_hat_label = self.label_vector(
            j_hat, "\\hat{\\jmath}", 
            color = Y_COLOR, 
            label_scale_val = 1
        )
        self.dither()

        x, y = new_array.get_mob_matrix().flatten()
        for coord, v, label, factor, shift_right in [
            (x, i_hat, i_hat_label, self.vector_coords[0], False), 
            (y, j_hat, j_hat_label, self.vector_coords[1], True)
            ]:
            faded_v = v.copy().fade(0.7)
            scaled_v = Vector(factor*v.get_end(), color = v.get_color())

            scaled_label = VMobject(coord.copy(), label.copy())
            scaled_label.arrange_submobjects(RIGHT, buff = 0.1)
            scaled_label.move_to(label, DOWN+RIGHT)
            scaled_label.shift((scaled_v.get_end()-v.get_end())/2)
            coord_copy = coord.copy()
            self.play(
                Transform(v.copy(), faded_v),
                Transform(v, scaled_v),
                Transform(VMobject(coord_copy, label), scaled_label),
            )
            self.dither()
            if shift_right:
                group = VMobject(v, coord_copy, label)
                self.play(ApplyMethod(
                    group.shift, self.vector_coords[0]*RIGHT
                ))
        self.dither()


    def show_symbolic_sum(self, new_array, vector):
        new_mob = TexMobject([
            "(%d)\\hat{\\imath}"%self.vector_coords[0], 
            "+", 
            "(%d)\\hat{\\jmath}"%self.vector_coords[1]
        ])
        new_mob.move_to(new_array)
        new_mob.shift_onto_screen()
        i_hat, plus, j_hat = new_mob.split()
        i_hat.highlight(X_COLOR)
        j_hat.highlight(Y_COLOR)

        self.play(Transform(new_array, new_mob))
        self.dither()
        


class CoordinatesAsScalarsExample2(CoordinatesAsScalars):
    CONFIG = {
        "vector_coords" : [-5, 2]
    }

    def construct(self):
        self.add_axes()
        basis_vectors = self.get_basis_vectors()
        labels = self.get_basis_vector_labels()
        self.add(*basis_vectors)
        self.add(*labels)
        text = TextMobject("""
            $\\hat{\\imath}$ and $\\hat{\\jmath}$ 
            are the ``basis vectors'' \\\\
            of the $xy$ coordinate system
        """)
        text.scale_to_fit_width(SPACE_WIDTH-1)
        text.to_corner(UP+RIGHT)
        VMobject(*text.split()[:2]).highlight(X_COLOR)
        VMobject(*text.split()[5:7]).highlight(Y_COLOR)
        self.play(Write(text))
        self.dither(2)
        self.remove(*basis_vectors + labels)
        CoordinatesAsScalars.construct(self)











