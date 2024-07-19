library vunit_lib;
context vunit_lib.vunit_context;
use vunit_lib.check_pkg.all;

library ieee;
use ieee.std_logic_1164.all;

entity fulladder_tb is
  generic (runner_cfg : string);
end entity;

architecture tb of fulladder_tb is

component fulladder is
    port (
        a, b, cin: in std_logic;
        s, cout: out std_logic
    );
    end component;

    signal a, b, cin, s, cout: std_logic;
    signal input: std_logic_vector(2 downto 0);
    signal output: std_logic_vector(1 downto 0);

    begin
        dut: fulladder port map (a => a, b => b, cin => cin, s => s, cout => cout);

        a <= input(0);
        b <= input(1);
        cin <= input(2);
        output <= cout & s;
        main : process
  begin
    test_runner_setup(runner, runner_cfg);
    input <= "000";
    wait for 1 ns;
    check(output = "00");
    test_runner_cleanup(runner); -- Simulation ends here
  end process;
end architecture;