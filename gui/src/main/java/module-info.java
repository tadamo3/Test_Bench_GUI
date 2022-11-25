module testbench {
    requires javafx.controls;
    requires javafx.fxml;

    opens testbench to javafx.fxml;
    exports testbench;
}
