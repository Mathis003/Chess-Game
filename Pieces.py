from Assets import dico_board, LIST_BLACK_PIECES, LIST_WHITE_PIECES, pygame, white_queen_image, black_queen_image
from all_pieces import Pawn, Queen, King

class Pieces:

    def __init__(self, king_white, king_black):
        self.king_white = king_white
        self.king_black = king_black
        self.dico_list_pieces = {1 : LIST_WHITE_PIECES, -1 : LIST_BLACK_PIECES}

    def King_with_his_Tile(self, piece_moved):
        """Return the king piece and his tile (opponent to the piece moved)."""
        if piece_moved.color == 1:
            king, tile_king = self.king_black, self.king_black.tile
        if piece_moved.color == -1:
            king, tile_king = self.king_white, self.king_white.tile
        return king, tile_king

    def King_ownChess(self, king_piece, move_tile):
        l_remove_from_list = []
        save_color_case = dico_board[move_tile][2]
        dico_board[move_tile][2] = 0
        for piece in self.dico_list_pieces[- king_piece.color]:
            new_list_possible_moves = piece.update_possible_moves()
            if move_tile in new_list_possible_moves:
                l_remove_from_list.append(move_tile)
                break
        dico_board[move_tile][2] = save_color_case

        return l_remove_from_list

    def CheckOwnChess_pieces(self, own_piece, king_tile):
        """Return if the own move put the king in Chess."""
        for piece in self.dico_list_pieces[- own_piece.color]:  # dico_board[piece.tile][3]
            if own_piece.tile in dico_board[piece.tile][3]:

                if type(own_piece) != type(self.king_white): # If the piece is not the king
                    # Simu
                    save_possible_moves_piece = dico_board[piece.tile][3]
                    save_color_piece = dico_board[piece.tile][2]
                    dico_board[piece.tile][2] = 0
                    new_list_possible_moves = piece.update_possible_moves()
                    if king_tile in new_list_possible_moves:
                        dico_board[piece.tile][3] = []
                    else:
                        dico_board[piece.tile][3] = save_possible_moves_piece
                    dico_board[piece.tile][2] = save_color_piece
                else: # If the piece is the king

                    all_possible_moves_piece = dico_board[own_piece.tile][3]
                    l_to_remove_move_tile = []

                    # See if the king can move to ESCAPE
                    dico_board[own_piece.tile][2] = 0
                    for move_tile in all_possible_moves_piece:
                        # Check with a simulation if the king can escape by moving => If not, remove the move_tile !
                        # Changes for the simu
                        save_color_tile = dico_board[move_tile][2]
                        dico_board[move_tile][2] = own_piece.color
                        # Check the simu
                        new_list_possible_moves_piece = piece.update_possible_moves()
                        if move_tile in new_list_possible_moves_piece:
                            l_to_remove_move_tile.append(move_tile)
                        # Reset
                        dico_board[own_piece.tile][2] = own_piece.color
                        dico_board[move_tile][2] = save_color_tile

                    # Remove the move_tile from the list of possible move of the piece (if necessary)
                    for move_tile in l_to_remove_move_tile:
                        dico_board[own_piece.tile][3].remove(move_tile)

    def TileBetweenEmpty(self, list_tile):
        """Check if the tiles in the "list_tile" are all empty => return True, False otherwise."""
        for tile in list_tile:
            if dico_board[tile][2] != 0:
                return False
        return True

    def ChessTileBetween(self, list_tile, king_piece):
        """Check if the tiles in the "list_tile" are all not in Check => return True, False otherwise."""
        list_tile.append((7, 4))
        for piece in self.dico_list_pieces[- king_piece.color]:
            list_possible_moves = piece.update_possible_moves()
            for tile in list_tile:
                if tile in list_possible_moves:
                    return True
        return False

    def CastlingStroke(self, king_piece):
        if king_piece.color == 1:
            list_tile_leftstroke = [(7, 5), (7, 6)]
            list_tile_rightstroke = [(7, 3), (7, 2), (7, 1)]
            tile_to_append_left = (7, 6)
            tile_to_append_right = (7, 2)
        if king_piece.color == -1:
            list_tile_leftstroke = [(0, 5), (0, 6)]
            list_tile_rightstroke = [(0, 3), (0, 2), (0, 1)]
            tile_to_append_left = (0, 6)
            tile_to_append_right = (0, 2)

        if king_piece.Rook_LeftStroke():
            if self.TileBetweenEmpty(list_tile_leftstroke):
                if not self.ChessTileBetween(list_tile_leftstroke, king_piece):
                    dico_board[king_piece.tile][3].append(tile_to_append_left)
        if king_piece.Rook_RightStroke():
            if self.TileBetweenEmpty(list_tile_rightstroke):
                if not self.ChessTileBetween(list_tile_rightstroke, king_piece):
                    dico_board[king_piece.tile][3].append(tile_to_append_right)

    def basics_possible_moves(self, moved_piece):
        """Update the basics possible moves of the pieces."""
        for piece in self.dico_list_pieces[- moved_piece.color]: # Loop for each piece of the good color
            dico_board[piece.tile][3] = piece.update_possible_moves()  # Update possible moves of the piece

            if isinstance(piece, type(King([7, 4], 1, True, 0, 0))): # If the piece is the king
                self.CastlingStroke(piece) # Update the possible moves of the king if he can do the "Castling" stroke

    def Promotion_Pawn(self, piece, new_tile):
        """ If the piece is a Pawn and move to the last line, the pawn must be promoted to a Queen => Return True."""
        if type(piece) == type(Pawn([6, 0], 1, True)):
            if piece.color == 1: # Check if the pawn is white
                if new_tile[0] == 0: # If the pawn can move to the last line on the board
                    return True
            if piece.color == -1: # Check if the pawn is black
                if new_tile[0] == 7: # If the pawn can move to the first line on the board
                    return True
        return False

    def PromotePawn_into_Queen(self, piece, new_tile):
        """Promote the pawn into a Queen"""
        if piece.color == 1: # If the piece is white
            image_queen = white_queen_image
            list_piece = LIST_WHITE_PIECES
        else:
            image_queen = black_queen_image
            list_piece = LIST_BLACK_PIECES

        new_queen = Queen(new_tile, piece.color, True)
        self.remove_from_list_piece_eaten(new_tile)
        # Change the object in the dictionary
        dico_board[piece.tile] = [None, None, 0, []] # Reset the tile of the pawn from the dico_board
        dico_board[new_tile] = [new_queen, image_queen, piece.color, []]  # Add the queen to the dico_board
        # Update LIST OF PIECES
        list_piece.remove(piece) # Remove the pawn from the list of pieces
        list_piece.append(new_queen) # Add the queen to the list of pieces

    def PieceTouchPieceMoved(self, piece_moved, current_tile):
        """Return the list of pieces (the same color than the piece moved one) that are touching the piece moved if she moves."""
        list_pieces = []
        for piece in self.dico_list_pieces[piece_moved.color]:
            new_possible_moves = piece.update_possible_moves()
            if current_tile in new_possible_moves:
                list_pieces.append(piece)
        return list_pieces

    def CheckOpponent(self, piece_moved, current_tile):
        """Check if the opponent is in check => return True, False otherwise."""
        tile_king = self.King_with_his_Tile(piece_moved)[1]
        list_pieces_to_test = self.PieceTouchPieceMoved(piece_moved, current_tile) # Get the list of pieces that are touching the piece moved
        if piece_moved not in list_pieces_to_test:
            list_pieces_to_test.append(piece_moved) # Add the piece moved to the list of pieces to test
        for piece in list_pieces_to_test: # Loop for each piece of the list
            new_list_possible_moves = piece.update_possible_moves() # Update the possible moves of the piece moved
            if tile_king in new_list_possible_moves:
                return True, piece
        return False, None

##############################################################################################################################
    ############################################################################################################################## PAS FAIS POUR LE ROI LUI MEME ###############################################################################################################################
    def ReUpdate_ToNot_OwnChess(self, piece_moved):
        if piece_moved.color == 1:
            tile_king = self.king_black.tile
        if piece_moved.color == -1:
            tile_king = self.king_white.tile

        for piece in self.dico_list_pieces[- piece_moved.color]: # Loop for each piece of the good color
            l_to_remove_from_the_list = []
            if not isinstance(piece, type(King([7, 4], 1, True, 0, 0))): # If the piece is the king
                list_possible_moves = piece.update_possible_moves() # Update possible moves of the piece
                if list_possible_moves != []:
                    # Check if the piece protect the king => If not, ignore all of this function!
                    dico_board[piece.tile][2] = 0 # Simulate that the piece isn't there to see if the piece protect the king (being there) or not
                    for piece_opponent in self.dico_list_pieces[piece_moved.color]:
                        new_list_possible_moves = piece_opponent.update_possible_moves() # Update possible moves of the piece
                        if len(l_to_remove_from_the_list) == len(list_possible_moves):
                            break
                        if tile_king in new_list_possible_moves: # If the piece protect the king => Be careful
                            for move_tile in list_possible_moves:
                                if move_tile in l_to_remove_from_the_list:
                                    break
                                save_color_tile = dico_board[move_tile][2]
                                dico_board[move_tile][2] = piece.color
                                new_list_possible_moves = piece_opponent.update_possible_moves()  # Update possible moves of the piece
                                if tile_king in new_list_possible_moves:
                                    l_to_remove_from_the_list.append(move_tile)
                                dico_board[move_tile][2] = save_color_tile

                dico_board[piece.tile][2] = piece.color
                for move_tile in l_to_remove_from_the_list:
                    dico_board[piece.tile][3].remove(move_tile)

    def UpdateKingMoves_inCheck(self, piece_moved):
        """Update the possible moves of the king if he is in check."""
        king_chess = self.King_with_his_Tile(piece_moved)[0]  # Get the king's piece (opponent to the piece moved)
        l_to_remove_move_tile = []
        for move_tile in dico_board[king_chess.tile][3]: # Loop for each possible move of the king
            dico_board[king_chess.tile][2] = 0 # Simulate that the king isn't there
            save_color_tile = dico_board[move_tile][2] # Save the color of the tile's moved
            dico_board[move_tile][2] = king_chess.color # Simulate that the king is there
            for piece in self.dico_list_pieces[piece_moved.color]: # Loop for each piece of the opponent color
                new_all_possible_moves = piece.update_possible_moves() # Update possible moves of the piece
                if move_tile in new_all_possible_moves: # If the king is also in Check here
                    l_to_remove_move_tile.append(move_tile) # Add the move tile to the list of move tile to remove
                    dico_board[move_tile][2] = save_color_tile # Reset the color of the tile's moved
                    break # Break the loop for each piece of the opponent color => to change the move tiled
            dico_board[move_tile][2] = save_color_tile # Reset the color of the tile's moved

        dico_board[king_chess.tile][2] = king_chess.color # Reset the color of the tile's king
        # Remove the move_tile from the list of possible move of the piece (if necessary)
        for move_tile in l_to_remove_move_tile: # Loop for each move tile to remove
            dico_board[king_chess.tile][3].remove(move_tile) # Remove the move tile from the list of possible moves of the king

    def CheckMod_reupdate_possibles_move(self, piece_that_check):
        """Update all the possible move if the king is in Chess."""

        king_chess = self.King_with_his_Tile(piece_that_check)[0] # Get the king's piece (opponent to the piece moved)
        for piece in self.dico_list_pieces[- piece_that_check.color]: # Loop for each piece of the king's color
            all_possible_moves_piece = dico_board[piece.tile][3] # Get the possible moves of the piece
            l_to_remove_move_tile = []
            if type(piece) == type(self.king_white): # If the piece is the king
                self.UpdateKingMoves_inCheck(piece_that_check) # Update the possible moves of the king BEING in check!
            else: # If the piece is not the king
                # See if the piece can move to PROTECT the king
                for move_tile in all_possible_moves_piece: # Loop for each possible move of the piece
                    if move_tile != piece_that_check.tile:
                        # Check with a simulation if the piece can protect the king by moving => If not, remove the move_tile !
                        save_color_tile = dico_board[move_tile][2]
                        dico_board[move_tile][2] = - piece_that_check.color # Simulate that the piece move to see if the piece protect the king (being there) or not
                        new_list_possible_moves_piece = piece_that_check.update_possible_moves() # Update possible moves of the piece who put the king in check
                        if king_chess.tile in new_list_possible_moves_piece: # If the piece doesn't protect the king
                            l_to_remove_move_tile.append(move_tile) # Add to the list to remove all the move that doesn't protect the king
                        dico_board[move_tile][2] = save_color_tile # Reset the color of the tile

                # Remove the move_tile from the list of possible move of the piece
                for move_tile in l_to_remove_move_tile:
                    dico_board[piece.tile][3].remove(move_tile)

    def Check_Checkmate(self, piece_moved):
        """Check if the king is in checkmate."""
        for piece in self.dico_list_pieces[- piece_moved.color]:
            if dico_board[piece.tile][3] != []:
                return False
        return True

    def remove_from_list_piece_eaten(self, new_tile):
        # Remove the object (in the pieces list) from the old tile
        if dico_board[new_tile][0] != None: # If the tile contain a piece (= isn't empty)
            if dico_board[new_tile][2] == 1: # If the piece is white
                LIST_WHITE_PIECES.remove(dico_board[new_tile][0]) # Remove the white piece from the list of pieces
            elif dico_board[new_tile][2] == -1: # If the piece is black
                LIST_BLACK_PIECES.remove(dico_board[new_tile][0]) # Remove the black piece from the list of pieces

    def update_dico_board_basic_stroke(self, piece, current_tile, new_tile):
        # Update dico_board
        dico_board[new_tile] = [piece, dico_board[current_tile][1], dico_board[current_tile][2], []]
        dico_board[current_tile] = [None, None, 0, []]

    def move_pawn(self, pawn_piece, current_tile, new_tile):
        if new_tile == (current_tile[0] - pawn_piece.color, current_tile[1] + 1) or new_tile == (current_tile[0] - pawn_piece.color, current_tile[1] - 1):  # If the pawn move to an empty tile to eat an opponent piece ("En Passant")
            # Stroke "En Passant"
            tile_piece_eaten = (current_tile[0], new_tile[1])
            piece_eaten = dico_board[tile_piece_eaten][0]
            # Update the list of pieces (remove the piece eaten)
            self.dico_list_pieces[- pawn_piece.color].remove(piece_eaten)

            # Update dico_board
            self.update_dico_board_basic_stroke(pawn_piece, current_tile, new_tile)
            dico_board[tile_piece_eaten] = [None, None, 0, []]

        else:  # If the pawn move to an empty tile to move forward
            self.update_dico_board_basic_stroke(pawn_piece, current_tile, new_tile)

        if pawn_piece.first_move:  # If the pawn is on his first move, it can move 2 tiles
            if abs(current_tile[0] - new_tile[0]) == 2:  # If the pawn has moved 2 tiles
                pawn_piece.just_moved = True
        else:  # If the pawn is not on his first move anymore
            pawn_piece.just_moved = False

    def move_king(self, king_piece, current_tile, new_tile):
        if king_piece.first_move:  # If the king is on his first move
            if new_tile == (7, 6):  # Right Castling
                # Update dico_board for the special stroke "Right Castling"
                dico_board[(7, 6)] = [dico_board[(7, 4)][0], dico_board[(7, 4)][1], dico_board[(7, 4)][2], []]
                dico_board[(7, 4)] = [None, None, 0, []]
                dico_board[(7, 5)] = [dico_board[(7, 7)][0], dico_board[(7, 7)][1], dico_board[(7, 7)][2], []]
                dico_board[(7, 7)] = [None, None, 0, []]
                rook_piece = dico_board[(7, 5)][0]
                rook_piece.tile = (7, 5)  # Update the rook's tile
                rook_piece.first_move = False  # The rook has moved

            elif new_tile == (7, 2):  # Left Castling
                # Update dico_board for the special stroke "Left Castling"
                dico_board[(7, 2)] = [dico_board[(7, 4)][0], dico_board[(7, 4)][1], dico_board[(7, 4)][2], []]
                dico_board[(7, 4)] = [None, None, 0, []]
                dico_board[(7, 3)] = [dico_board[(7, 0)][0], dico_board[(7, 0)][1], dico_board[(7, 0)][2], []]
                dico_board[(7, 0)] = [None, None, 0, []]
                rook_piece = dico_board[(7, 3)][0]
                rook_piece.tile = (7, 3)  # Update the rook's tile
                rook_piece.first_move = False  # The rook has moved

            elif new_tile == (0, 6):  # Right Castling
                # Update dico_board for the special stroke "Right Castling"
                dico_board[(0, 6)] = [dico_board[(0, 4)][0], dico_board[(0, 4)][1], dico_board[(0, 4)][2], []]
                dico_board[(0, 4)] = [None, None, 0, []]
                dico_board[(0, 5)] = [dico_board[(0, 7)][0], dico_board[(0, 7)][1], dico_board[(0, 7)][2], []]
                dico_board[(0, 7)] = [None, None, 0, []]
                rook_piece = dico_board[(0, 5)][0]
                rook_piece.tile = (0, 5)  # Update the rook's tile
                rook_piece.first_move = False  # The rook has moved

            elif new_tile == (0, 2):  # Left Castling
                # Update dico_board for the special stroke "Left Castling"
                dico_board[(0, 2)] = [dico_board[(0, 4)][0], dico_board[(0, 4)][1], dico_board[(0, 4)][2], []]
                dico_board[(0, 4)] = [None, None, 0, []]
                dico_board[(0, 3)] = [dico_board[(0, 0)][0], dico_board[(0, 0)][1], dico_board[(0, 0)][2], []]
                dico_board[(0, 0)] = [None, None, 0, []]
                rook_piece = dico_board[(0, 3)][0]
                rook_piece.tile = (0, 3)  # Update the rook's tile
                rook_piece.first_move = False  # The rook has moved

            else:  # If the king move to a tile (other than the special's tile for stroke "Castling")
                self.remove_from_list_piece_eaten(new_tile)  # Remove the piece eaten from the list of pieces (if there is one)
                self.update_dico_board_basic_stroke(king_piece, current_tile, new_tile)

        else:  # If the king is not on his first move anymore
            self.remove_from_list_piece_eaten(new_tile)  # Remove the piece eaten from the list of pieces (if there is one)
            self.update_dico_board_basic_stroke(king_piece, current_tile, new_tile)

    def move_other_pieces(self, moved_piece, current_tile, new_tile):
        self.remove_from_list_piece_eaten(new_tile)  # Remove the piece eaten from the list of pieces (if there is one)
        self.update_dico_board_basic_stroke(moved_piece, current_tile, new_tile)

    def move_piece(self, piece, current_tile, new_tile):
        """Move the piece to the new tile and update all the necessary elements."""

        if isinstance(piece, type(Pawn((6, 0), 1, True))) and dico_board[new_tile][2] == 0: # If the piece is a pawn that move to an empty tile
            self.move_pawn(piece, current_tile, new_tile)

        elif isinstance(piece, type(self.king_white)): # If the piece is the king
            self.move_king(piece, current_tile, new_tile)

        else: # If the piece is not a pawn or a king
            self.move_other_pieces(piece, current_tile, new_tile)

        # Update position of the moved piece on the board => piece.tile = new_tile
        piece.tile = new_tile

        # Update the first move of the piece
        if piece.first_move: # If the piece is on its first move
            piece.first_move = False # The pawn is not on its first move anymore

    def JustMovedPawn(self, piece):
        """Check if the pawn just moved => If yes, return True."""
        if isinstance(piece, type(Pawn((6, 0), 1, True))):
            if piece.just_moved:
                return True
        return False