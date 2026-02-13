class SoundServer < Formula
  include Language::Python::Virtualenv

  desc "HTTP server for playing audio notifications on macOS"
  homepage "https://github.com/deanputney/sound-server"
  url "https://files.pythonhosted.org/packages/source/s/sound-server/sound-server-2.0.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"
  license "MIT"

  depends_on "python@3.12"

  resource "annotated-types" do
    url "https://files.pythonhosted.org/packages/ee/67/531ea369ba64dcff5ec9c3402f9f51bf748cec26dde048a2f973a4eea7f5/annotated_types-0.7.0.tar.gz"
    sha256 "aff07c09a53a08bc8cfccb9c85b05f1aa9a2a6f23728d790723543408344ce89"
  end

  resource "click" do
    url "https://files.pythonhosted.org/packages/96/d3/f04c7bfcf5c1862a2a5b845c6b2b360488cf47af55dfa79c98f6a6bf98b5/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
  end

  resource "fastapi" do
    url "https://files.pythonhosted.org/packages/7b/5e/bf0471f14bf6ebfbee8208148a3396d1a23298531a6cc10776c59f4c0f87/fastapi-0.115.0.tar.gz"
    sha256 "f93b4ca3529a8ebc6fc3fcf710e5efa8de3df9b41570958abf1d97d843138004"
  end

  resource "h11" do
    url "https://files.pythonhosted.org/packages/f5/38/3af3d3633a34a3316095b39c8e8fb4853a28a536e55d347bd8d8e9a14b03/h11-0.14.0.tar.gz"
    sha256 "8f19fbbe99e72420ff35c00b27a34cb9937e902a8b810e2c88300c6f0a3b699d"
  end

  resource "pydantic" do
    url "https://files.pythonhosted.org/packages/e9/78/58c36d0cf331b659d0ccd99175e3523c457b4f8e67cb92a8fdc22ec1667c/pydantic-2.10.0.tar.gz"
    sha256 "0aca0f045ff6e2f097f1fe89521115335f15049eeb8a7bef3dafe4b19a74e289"
  end

  resource "pydantic-core" do
    url "https://files.pythonhosted.org/packages/d1/cd/8331ae216bcc5a3f2d4c6b941c9f63de647e2700d38133f4f7e0132a00c4/pydantic_core-2.27.0.tar.gz"
    sha256 "f57783fbaf648205ac50ae7d646f27582fc706be3977e87c3c124e7a92407b10"
  end

  resource "starlette" do
    url "https://files.pythonhosted.org/packages/c4/68/79977123bb7be889ad680d79a40f339082c1978b5cfcf62c2d8d196873ac/starlette-0.52.1.tar.gz"
    sha256 "834edd1b0a23167694292e94f597773bc3f89f362be6effee198165a35d62933"
  end

  resource "typing-extensions" do
    url "https://files.pythonhosted.org/packages/72/94/1a15dd82efb362ac84269196e94cf00f187f7ed21c242792a923cdb1c61f/typing_extensions-4.15.0.tar.gz"
    sha256 "0cea48d173cc12fa28ecabc3b837ea3cf6f38c6d1136f85cbaaf598984861466"
  end

  resource "uvicorn" do
    url "https://files.pythonhosted.org/packages/4b/4d/938bd85e5bf2edeec766267a5015ad969730bb91e31b44021dfe8b22df6c/uvicorn-0.34.0.tar.gz"
    sha256 "404051050cd7e905de2c9a7e61790943440b3416f49cb409f965d9dcd0fa73e9"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    # Test that the command exists and shows help
    output = shell_output("#{bin}/sound-server --help")
    assert_match "Sound Server", output

    # Test that the --check flag works (server should not be running in test)
    system "#{bin}/sound-server", "--check"
    assert_equal 1, $?.exitstatus
  end
end
