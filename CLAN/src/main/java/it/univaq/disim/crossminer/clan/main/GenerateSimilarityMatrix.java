package it.univaq.disim.crossminer.clan.main;

import java.io.*;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Arrays;

import org.apache.commons.math3.linear.RealMatrix;

import it.univaq.disim.crossminer.matrix.CosineSimilarity;
import it.univaq.disim.crossminer.matrix.LSA;

public class GenerateSimilarityMatrix {

    public void generate(ArrayList<String> path_list, String operation, ArrayList jdk, String matrix_name) throws IOException, URISyntaxException {

        MatrixManager manager = new MatrixManager();
        LSA lsa = new LSA();
        ArrayList<ArrayList<Double>> occurrencies_list = new ArrayList<ArrayList<Double>>();

        /*
         * parsing
         */
        occurrencies_list = manager.createFiles(path_list, operation, jdk);

        RealMatrix m = manager.createMatrix(occurrencies_list);

        System.out.println("Numero di Termini: " + m.getRowDimension());

        /*
         * LSA
         */
        m = lsa.algorithm(m);

        /*
         * Similarity
         */
        CosineSimilarity csm = new CosineSimilarity();
        m = csm.CS(m);

        /*
         * scrittura su file
         */
        File file = new File("results" + operation + ".txt");
        FileWriter fileWriter = new FileWriter(file);
        double[][] arr = m.getData();
        System.out.println(Arrays.deepToString(m.getData()));
        for (int i = 0; i < m.getRowDimension(); i++) {
            fileWriter.write(m.getRowMatrix(i).toString() + "\n");
        }


        BufferedWriter br = new BufferedWriter(new FileWriter(matrix_name));
        StringBuilder sb = new StringBuilder();
        sb.append("a,");
        for (int i = 0; i < path_list.size(); i++) {
            String path = path_list.get(i);
            sb.append(path.substring(path.lastIndexOf('\\') + 1).trim());
            if (i != path_list.size() - 1)
                sb.append(",");
        }
        sb.append("\n");
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr.length; j++) {
                if (j == 0) {
                    String path = path_list.get(i);
                    sb.append(path.substring(path.lastIndexOf('\\') + 1).trim());
                    sb.append(",");
                } /*else {*/
                    double num = Math.abs(arr[i][j]);
                    sb.append(num);
                /*}*/
                if (j != arr.length - 1)
                    sb.append(",");
            }
            sb.append("\n");
        }
        br.write(sb.toString());
        br.close();
        fileWriter.flush();
        fileWriter.close();
    }

}
