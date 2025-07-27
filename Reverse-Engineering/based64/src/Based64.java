import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Arrays;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;

public class Based64 {
    static final String CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    static final int[][] TABLE = {{22, 2, 15, 5, 19, 17, 11, 61}, {60, 59, 27, 18, 7, 23, 21, 44}, {26, 34, 58, 38, 37, 4, 14, 20}, {29, 39, 13, 56, 57, 47, 9, 46}, {54, 62, 33, 42, 48, 12, 45, 53}, {35, 55, 36, 25, 52, 41, 49, 8}, {24, 50, 16, 6, 40, 28, 3, 63}, {51, 0, 1, 30, 31, 32, 10, 43}};
    static boolean[][] visited = new boolean[8][8];
    static int[][] map = {{63, 63, 63, 63, 63, 62, 63, 63}, {63, 63, 62, 62, 61, 61, 59, 63}, {55, 63, 63, 61, 63, 62, 62, 63}, {63, 62, 61, 61, 61, 59, 61, 63}, {63, 63, 60, 61, 63, 60, 51, 54}, {62, 55, 39, 35, 61, 58, 43, 52}, {44, 48, 56, 54, 54, 31, 23, 27}, {58, 46, 48, 39, 23, 31, 33, 21}};

    // Count the number of onward valid knight moves from (x, y)
    static int co(List<List<Integer>> board, int x, int y, 
                            int[][] dir) {
        int count = 0;
        int n = board.size();

        // Check all 8 possible dir
        for (int[] d : dir) {
            int nx = x + d[0];
            int ny = y + d[1];

            // If next cell is inside board and unvisited
            if (nx >= 0 && ny >= 0 && nx < n && ny < n &&
                board.get(nx).get(ny) == -1) {
                count++;
            }
        }
        return count;
    }

    // Generate possible knight moves from (x, y), sorted by
    // least onward options
    static List<int[]> gsm(List<List<Integer>> board, int x, 
                                      int y, int[][] dir) {
        List<int[]> moves = new ArrayList<>();
        int n = board.size();

        for (int i = 0; i < dir.length; i++) {
            int nx = x + dir[i][0];
            int ny = y + dir[i][1];

            if (nx >= 0 && ny >= 0 && nx < n && ny < n && 
                board.get(nx).get(ny) == -1) {
                // Store onward move count and direction index
                moves.add(new int[]{co(board, nx, ny, dir), i});
            }
        }

        // Sort by Warnsdorff's heuristic (fewer onward moves first)
        moves.sort(Comparator.comparingInt(a -> a[0]));
        return moves;
    }

    // Recursive function to explore knight's tour from (x, y)
    static boolean ktu(int x, int y, int step, int n,
                                    List<List<Integer>> board,  
                                    int[][] dir) {
        if (step == n * n) return true;

        List<int[]> moves = gsm(board, x, y, dir);
        for (int[] move : moves) {
            int dirIdx = move[1];
            int nx = x + dir[dirIdx][0];
            int ny = y + dir[dirIdx][1];
            
            // Make move
            board.get(nx).set(ny, step);  
            if (ktu(nx, ny, step + 1, n, board, dir))
                return true;
                
            // BacknightTourrack
            board.get(nx).set(ny, -1); 
        }
        return false;
    }
    
    static int[] kt(int x, int y) {
        List<List<Integer>> board = new ArrayList<>(8);
        for (int i = 0; i < 8; ++i) {
            List<Integer> row = new ArrayList<>(Collections.nCopies(8, -1));
            board.add(row);
        }
        
        int[][] dir = {
            {2, 1}, {1, 2}, {-1, 2}, {-2, 1},
            {-2, -1}, {-1, -2}, {1, -2}, {2, -1}
        };
        
        board.get(x).set(y, 0);

        // System.out.printf("x = %d, y = %d\n", x, y);
        if (!ktu(x, y, 1, 8, board, dir)) {
            return new int[] {y, x};
        }
        
        // boolean done = false;
        // boolean restart = false;
        int target = map[x][y];
        // while (!done) {
            for (int cx = 0; cx < 8; cx++) {
                for (int cy = 0; cy < 8; cy++) {
                    if (board.get(cx).get(cy) == target) {
                        // if (visited[cx][cy]) {
                            // target = (target-1) < 0 ? 0 : target-1;
                            // restart = true;
                            // break;
                        // }
                        // visited[cx][cy] = true;
                        // System.out.printf("x = %d, y = %d, cx = %d, cy = %d\n", x, y, cx, cy);
                        return new int[] {cx, cy};
                    }
                }
                
                // if (restart) {
                    // restart = false;
                    // break;
                // }
                
                // if (done) {
                    // break;
                // }
            }
        // }
        
        return new int[] {y, x};
    }
    
    static byte[] encode(byte[] inputBytes) {
        String input = new String(inputBytes);
        String pad = "";
        int c = input.length() % 3;
        for (; c > 0 && c < 3; c++) {
            pad += "=";
            input += "\0";
        }
        StringBuilder res = new StringBuilder(input.length() / 3);
        
        for (c = 0; c < input.length(); c += 3) {
            int n = (input.charAt(c) << 16) + (input.charAt(c+1) << 8) + (input.charAt(c+2));
            
            int n1 = (n >> 18) & 0x3F, n2 = (n >> 12) & 0x3F, n3 = (n >> 6) & 0x3F, n4 = n & 0x3F;
            
            System.out.printf("n = %d, n1 = %d, n2 = %d, n3 = %d, n4 = %d\n", n, n1, n2, n3, n4);
            
            int[] coord1 = kt(n1/8, n1%8);
            int[] coord2 = kt(n2/8, n2%8);
            int[] coord3 = kt(n3/8, n3%8);
            int[] coord4 = kt(n4/8, n4%8);
            
            System.out.printf("ch1 = %d, ch2 = %d, ch3 = %d, ch4 = %d\n", TABLE[coord1[0]][coord1[1]], TABLE[coord2[0]][coord2[1]], TABLE[coord3[0]][coord3[1]], TABLE[coord4[0]][coord4[1]]);
            System.out.println("coord1 = " + Arrays.toString(coord1) + ", coord2 = " + Arrays.toString(coord2) + ", coord3 = " + Arrays.toString(coord3) + ", coord4 = " + Arrays.toString(coord4));
            
            char ch1 = CHARS.charAt(TABLE[coord1[0]][coord1[1]]);
            char ch2 = CHARS.charAt(TABLE[coord2[0]][coord2[1]]);
            char ch3 = CHARS.charAt(TABLE[coord3[0]][coord3[1]]);
            char ch4 = CHARS.charAt(TABLE[coord4[0]][coord4[1]]);
            
            res.append(ch1);
            res.append(ch2);
            res.append(ch3);
            res.append(ch4);
        }
        
        return (res.substring(0, res.length() - pad.length()) + pad).getBytes(StandardCharsets.UTF_8);
    }

    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));) {
            System.out.print("Enter filename to encode: ");
            String inputFileName = reader.readLine();
            
            if (inputFileName == null || inputFileName.isEmpty()) {
                System.err.println("Error: Filename must be provided");
                return;
            }

            String outputFileName = inputFileName + ".enc";

            byte[] fileBytes = Files.readAllBytes(Paths.get(inputFileName));
            
            byte[] encodedBytes = encode(fileBytes);
            Files.write(Paths.get(outputFileName), encodedBytes);
            
            System.out.println("File encoded successfully. Output: " + outputFileName);
        } catch (IOException e) {
            System.err.println("Error processing file: " + e.getMessage());
        }
    }
}