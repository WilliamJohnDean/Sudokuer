import sys
import pygame
from functools import reduce
import dlx

class Backtracker:
    def __init__(self, grid):
        self.grid = grid

    def solve_gui(self) -> bool:
        from Grid import find_empty, valid # Circular Import
        self.grid.update_model()
        find = find_empty(self.grid.model)

        if not find:
            return True
        else:
            row, col = find

        for i in range(1, self.grid.gamesize + 1):
            if valid(self.grid.model, i, (row, col), self.grid.gamesize):
                self.grid.model[row][col] = i
                self.grid.cubes[row][col].set(i)
                if self.grid.animate:    
                    self.grid.cubes[row][col].draw_change(self.grid.win, True)
                    self.grid.update_model()
                    pygame.display.update()

                if self.solve_gui():
                    return True

                self.grid.model[row][col] = 0
                self.grid.cubes[row][col].set(0)
                if self.grid.animate:
                    self.grid.update_model()
                    self.grid.cubes[row][col].draw_change(self.grid.win, False)
                    pygame.display.update()
                
        return False

class DLXsudoku(dlx.DLX):
    def __init__(self, grid):
        from numpy import sqrt
        self.grid = grid
        self.dimsq = grid.gamesize
        self.dim = int(sqrt(grid.gamesize))

        # Create the columns.
        ctr = 0
        cols = []
        # Create the row coverage, which determines that entry j appears in row i.
        for i in range(self.dimsq):
            cols += [(('r', i, j), ctr + j - 1) for j in range(1, self.dimsq + 1)]
            ctr += self.dimsq

        # Create the column coverage, which determines that entry j appears in column i.
        for i in range(self.dimsq):
            cols += [(('c', i, j), ctr + j - 1) for j in range(1, self.dimsq + 1)]
            ctr += self.dimsq

        # Create the grid coverage, which determines that entry k appears in grid i,j.
        for i in range(self.dim):
            for j in range(self.dim):
                cols += [(('g', i, j, k), ctr + k - 1) for k in range(1, self.dimsq + 1)]
                ctr += self.dimsq

        # Create the entry coverage, which determines that entry i,j in the grid is occupied.
        for i in range(self.dimsq):
            cols += [(('e', i, j), ctr + j) for j in range(self.dimsq)]
            ctr += self.dimsq
      
        # Create a dictionary from this, which maps column name to column index.
        sdict = dict(cols)
        dlx.DLX.__init__(self, [(colname[0], dlx.DLX.PRIMARY) for colname in cols])

        # Now create all possible rows.
        rowdict = {}
        self.lookupdict = {}
        for i in range(self.dimsq):
            for j in range(self.dimsq):
                for k in range(1, self.dimsq + 1):
                    val =  self.appendRow([sdict[('r', i, k)], sdict[('c', j, k)], sdict[('g', i // self.dim, j // self.dim, k)], sdict[('e', i, j)]], (i, j, k))
                    rowdict[(i,j,k)] = val
                    self.lookupdict[val] = (i,j,k)

        # Now we want to process grid, which we take to be a string of length 81 representing the puzzle.
        # An entry of 0 means blank.
        for i in range(self.dimsq):
            for j in range(self.dimsq):
                if self.grid.cubes[i][j].value != 0:
                    self.useRow(rowdict[(i, j, self.grid.cubes[i][j].value)])

    def createSolutionGrid(self, sol):
        '''Return a two dimensional grid representing the solution.'''
        solgrid = [['0'] * self.dimsq for i in range(self.dimsq)]
        for a in sol:
            i, j, k = self.N[a]
            solgrid[i][j] = k 
        return solgrid
        

    def solve_gui(self) -> bool:
        for sol in self.solve():
            solgrid = self.createSolutionGrid(sol)

        for i in range(self.dimsq):
            for j in range(self.dimsq):
                k = solgrid[i][j]
                self.grid.model[i][j] = k
                self.grid.cubes[i][j].set(k)
                self.grid.cubes[i][j].draw_change(self.grid.win, True)   
                self.grid.update_model()
        return True

    