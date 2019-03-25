class Dima < Formula
  include Language::Python::Virtualenv

  desc "CLI to view and kill running queries in postgres"
  homepage "https://github.com/Frameio/homebrew-dima"
  url "https://github.com/Frameio/homebrew-dima/raw/master/homebrew/dima-1.0.0.tar.gz"
  sha256 "d54f4d7267345954fe668b267625fbb6c452407d3689445922d51646125260ed"
  version "1.0.0"

  depends_on "python@2"
  depends_on "postgresql"

  bottle :unneeded

  resource "terminaltables" do
    url "https://files.pythonhosted.org/packages/9b/c4/4a21174f32f8a7e1104798c445dacdc1d4df86f2f26722767034e4de4bff/terminaltables-3.1.0.tar.gz"
    sha256 "4a21174f32f8a7e1104798c445dacdc1d4df86f2f26722767034e4de4bff"
  end

  resource "psycopg2" do
    url "https://files.pythonhosted.org/packages/c0/07/93573b97ed61b6fb907c8439bf58f09957564cf7c39612cef36c547e68c6/psycopg2-2.7.6.1.tar.gz"
    sha256 "27959abe64ca1fc6d8cd11a71a1f421d8287831a3262bd4cacd43bbf43cc3c82"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"dima", "--help"
  end
end
